import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi_pagination import Params
from src.models.leads_model import LeadModel
from src.exceptions import DatabaseException, NotFoundException, InvalidRequestException
from src.schemas.courses_schema import CourseCreate
from src.schemas.leads_schema import LeadCreate
from src.services.leads_manager import LeadsManager
from pydantic import ValidationError


class TestLeadsManager(unittest.TestCase):
    def setUp(self):
        self.db_session = Mock(spec=Session)
        self.manager = LeadsManager(self.db_session)

    def test_create_lead_success(self):
        lead_data = LeadCreate(
            full_name="Pedro Diaz",
            email="pedro@mail.com",
            address="123 calle",
            phone="+1234567890",
            registration_date=datetime.now(),
            courses=[CourseCreate(subject="Math", career="Engineering", year_of_enrollment=2023, times_taken=1)])

        mock_lead = Mock()
        mock_lead.id = 1
        self.db_session.commit.return_value = None
        self.db_session.refresh.side_effect = lambda x: setattr(x, 'id', 1)

        with patch.object(self.manager, '_add_courses_to_lead') as mock_add_courses:
            result = self.manager.create_lead(lead_data)

        self.assertIsInstance(result, LeadModel)
        self.assertEqual(result.full_name, lead_data.full_name)
        self.assertEqual(result.email, lead_data.email)
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.db_session.refresh.assert_called_once()
        mock_add_courses.assert_called_once_with(1, lead_data.courses)

    def test_create_lead_invalid_exception(self):
        lead_data = LeadCreate(
            full_name="Pedro Diaz",
            email="pedro@mail.com",
            address="123 calle",
            phone="+1234567890",
            registration_date=datetime.now()
        )

        self.db_session.add.side_effect = Exception("Database error")

        with self.assertRaises(InvalidRequestException):
            self.manager.create_lead(lead_data)

        self.db_session.rollback.assert_called_once()

    @patch('src.services.leads_manager.paginate')
    def test_get_leads_success(self, mock_paginate):
        params = Params(page=1, size=10)
        mock_paginate.return_value = Mock()

        result = self.manager.get_leads(params)

        self.assertEqual(result, mock_paginate.return_value)
        mock_paginate.assert_called_once()

    @patch('src.services.leads_manager.paginate')
    def test_get_leads_database_exception(self, mock_paginate):
        params = Params(page=1, size=10)
        mock_paginate.side_effect = Exception("Database error")

        with self.assertRaises(DatabaseException):
            self.manager.get_leads(params)

    def test_get_lead_by_id_success(self):
        lead_id = 1
        mock_lead = Mock(spec=LeadModel)
        mock_lead.id = lead_id
        mock_lead.full_name = "Pedro Diaz"
        mock_lead.email = "pedro@mail.com"

        self.db_session.query.return_value.filter.return_value.first.return_value = mock_lead

        result = self.manager.get_lead(lead_id)

        self.assertEqual(result, mock_lead)
        self.assertEqual(result.id, lead_id)
        self.assertEqual(result.full_name, "Pedro Diaz")
        self.assertEqual(result.email, "pedro@mail.com")

    def test_get_lead_by_id_not_found(self):
        lead_id = 999

        self.db_session.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(NotFoundException):
            self.manager.get_lead(lead_id)

    def test_create_lead_invalid_email_and_phone(self):
        invalid_lead_data = {
            "full_name": "John Doe",
            "email": "invalid-email",
            "address": "123 Main St",
            "phone": "123",
            "registration_date": datetime.now(),
            "courses": []
        }

        with self.assertRaises(ValidationError) as context:
            LeadCreate(**invalid_lead_data)

        errors = context.exception.errors()
        error_fields = [error["loc"][0] for error in errors]

        self.assertIn("email", error_fields)
        self.assertIn("phone", error_fields)


if __name__ == '__main__':
    unittest.main()
