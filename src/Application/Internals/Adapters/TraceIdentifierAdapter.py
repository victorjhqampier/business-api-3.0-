from Domain.Commons.Validators.ArifyValidator import ArifyValidator
from typing import Optional
from pydantic import BaseModel

class TraceIdentifierAdapter(BaseModel):
    DeviceIdentifier:Optional[str]
    MessageIdentifier:Optional[str]
    ChannelIdentifier:Optional[str]

class TraceIdentifierAdapterValidator (ArifyValidator):
    def __init__(self, x: TraceIdentifierAdapter) -> None:
        super().__init__()
        
        self.add_rules(
            self.field(x, x.DeviceIdentifier)
                .not_null().with_code("21001").with_message("Cannot be null")
                .not_empty().with_code("21002").with_message("Cannot be empty")
                .min_length(5).with_code("21004").with_message("Allowed minimum length")
                .max_length(42).with_code("21005").with_message("Allowed maximum length")
                .validate()
        )
        
        self.add_rules(
            self.field(x, x.MessageIdentifier)
                .not_null().with_code("21001").with_message("Cannot be null")
                .not_empty().with_code("21002").with_message("Cannot be empty")
                .min_length(5).with_code("21004").with_message("Allowed minimum length")
                .max_length(42).with_code("21005").with_message("Allowed maximum length")
                .validate()
        )

        self.add_rules(
            self.field(x, x.ChannelIdentifier)
                .not_null().with_code("21001").with_message("Cannot be null")
                .not_empty().with_code("21002").with_message("Cannot be empty")
                .min_length(5).with_code("21004").with_message("Allowed minimum length")
                .max_length(42).with_code("21005").with_message("Allowed maximum length")
                .validate()
        )
