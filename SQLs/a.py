from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class DDQLiteRule(BaseModel):
    rule_number: int
    source_table: Optional[str] = None
    source_datastore: str
    check_type: Literal['not_null', 'distinct_count', 'unique_check', 'within_set', 'query', 'drift']
    column_name: Optional[str] = None
    expected_value: Optional[int] = None
    source_query: Optional[str] = None
    target_query: Optional[str] = None
    target_datastore: Optional[str] = None
    drift_check_type: Optional[Literal['null_percent', 'standard_deviation', 'avg', 'z_score-cnt']] = None
    drift_threshold: Optional[float] = None

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values):
        check_type = values.get("check_type")

        # Validation for 'distinct_count', 'unique_check', 'within_set', 'not_null'
        if check_type in ['distinct_count', 'unique_check', 'within_set', 'not_null']:
            if not values.get("column_name"):
                raise ValueError(f"'column_name' is required for check_type '{check_type}'")
            if not values.get("source_table"):
                raise ValueError(f"'source_table' is required for check_type '{check_type}'") 
            if check_type in ['distinct_count'] and not values.get("expected_value"):
                raise ValueError(f"'expected_value' is required for check_type '{check_type}'")

        # Validation for 'query'
        if check_type == "query":
            if not values.get("source_query") or not values.get("target_query") or not values.get("target_datastore"):
                raise ValueError(f"'source_query', 'target_query', and 'target_datastore' are required for check_type 'query'")

        # Validation for 'drift'
        if check_type == "drift":
            required_fields = ["source_table", "column_name", "drift_check_type", "drift_threshold"]
            missing_fields = [field for field in required_fields if not values.get(field)]
            if missing_fields:
                raise ValueError(f"{', '.join(missing_fields)} are required for check_type 'drift'")

        return values
