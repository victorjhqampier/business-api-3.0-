from typing import Optional
from Domain.Commons.Validators.ArifyValidator import ArifyValidator
from Domain.Messages.InternalApiMessage import InternalApiMessage
from pydantic import BaseModel

class ExampleRequestAdaper(BaseModel):    
    channelIdentification: Optional[str] = None
    messageIdentification: Optional[str] = None
    deviceIdentifier: Optional[str] = None
    customerIdentificationNumber: Optional[str] = None
    identificationForAccount: Optional[str] = None

class ExampleRequestAdaperValidator (ArifyValidator):
    def __init__(self, obj: ExampleRequestAdaper):
        super().__init__()
        
        self.add_rules(
            self.field(obj, obj.channelIdentification)
                .not_null()
                .not_empty()
                .min_length(7)
                .max_length(30)
                .with_code("122")
                .with_message("Corrija el campo caray")
                .validate()
        )
        
        self.add_rules(
            self.field(obj, obj.messageIdentification)
                .not_null()
                .not_empty()
                .min_length(7)
                .max_length(30)
                .with_code("2")
                .validate()
        )

        self.add_rules(
            self.field(obj, obj.deviceIdentifier)
                .not_null()
                .not_empty()
                .min_length(7)
                .max_length(40)
                .with_code("3")
                .validate()
        )

        self.add_rules(
            self.field(obj, obj.customerIdentificationNumber)
                .not_null()
                .not_empty()
                .min_length(1)
                .max_length(10)
                .is_numeric()
                .with_code("15091")
                .with_message(InternalApiMessage._15091.value)
                .validate()
        )

        self.add_rules(
            self.field(obj, obj.identificationForAccount)
                .not_null()
                .not_empty()
                .min_length(10)
                .max_length(30)
                .with_code("15091")
                .validate()
        )