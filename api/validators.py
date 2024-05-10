from wtforms import Form, IntegerField, DecimalField, StringField, SelectField, BooleanField, validators
from api.utlis import MultiDict
class ItemForm(Form):
    itemCode = IntegerField("Item Code", validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    qty = IntegerField("Quantity", validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    discountType = SelectField("Discount Type", choices=[
        ("cost", "Cost"), ("percent", "Percent")], validators=[validators.DataRequired()])
    discountValue = DecimalField("Discount Value", validators=[validators.DataRequired(),
                                                            validators.NumberRange(min=0)])


class SalesForm(Form):
    isCredit = BooleanField("Is Credit", validators=[validators.DataRequired()])
    hasLoadingFee = BooleanField("Has Loading Fee", validators=[validators.DataRequired()])
    terms = SelectField("Terms", choices=["UPI", "CASH", "CREDIT"], validators=[validators.DataRequired()])
    transactionId = StringField("TransactionId")


class ProductForm(Form):
    name = StringField("Name", validators=[validators.DataRequired(), validators.Length(2, 15)])
    costPrice = DecimalField("Cost Price", validators=[validators.DataRequired(), validators.NumberRange(min=200, max=2000)])
    sellingPrice = DecimalField("Selling Price", validators=[validators.DataRequired(), validators.NumberRange(min=200, max=2000)])
    stock = IntegerField("Stock", validators=[validators.DataRequired(), validators.NumberRange(min=0, max=500)] )
    
    
class AddressForm(Form): 
    line1 = StringField("Line 1", validators=[validators.DataRequired()])
    line2 = StringField("Line 2", validators=[validators.DataRequired()])
    city = StringField("City", validators=[validators.DataRequired(), validators.Length(2)])
    pincode = IntegerField("Pincode", validators=[validators.DataRequired(), validators.NumberRange(min=100000, max=999999)] )
   
   
class CustomerForm(Form):
    name = StringField("Name", validators=[validators.DataRequired(), validators.Length(2, 15)])
    phone = StringField("Phone", validators=[validators.Optional(), validators.Length(10, 10)])
    email = StringField("Email", validators=[validators.Optional(), validators.Email()]) 
    balance = DecimalField("Balance", validators=[validators.Optional(), validators.NumberRange(min=1)])
    
    
def sales (data):
    try:
        sales = SalesForm(data)
        if not sales.validate():
            return False
        for item in data['items']:
            form = ItemForm(data=item)
            if not form.validate():
                return False
    except Exception as e:
        return False
    finally:
        return True
   
   
def customer(data:dict):
    try:
        form = CustomerForm(MultiDict(data))
        if not form.validate():
            return False
        for address in data['addresses']:
            addressform = AddressForm(address)
            if not addressform.validate():
                return False
    except Exception as e:
        return False
    finally:
        return True
    
    
def product(data: dict):
    out = ProductForm(MultiDict(data))
    if not out.validate():
        return False
    return True
