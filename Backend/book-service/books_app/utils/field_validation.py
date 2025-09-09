class FieldValidation:

    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate that all required fields are present and not empty"""
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(f"The following fields are required: {', '.join(missing_fields)}")