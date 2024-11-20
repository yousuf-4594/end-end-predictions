import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel, Field, ValidationError
import pandas as pd
import joblib
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from groq import Groq
from typing import List, Dict, Any
from sqlalchemy import text


from fastapi.middleware.cors import CORSMiddleware


# Load the saved model
model_filename = "random_forest_model.pkl"
loaded_model = joblib.load(model_filename)
print("Model loaded successfully!")
    

DATABASE_URL = "postgresql://postgres.fpaiiaawtsqbhtvkpavq:Blackpanther1290!@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CustomerModel(Base):
    __tablename__ = "customers"
    customer_id = Column(Text, primary_key=True)
    gender = Column(Text)
    is_senior_citizen = Column(Boolean)
    has_partner = Column(Boolean)
    has_dependents = Column(Boolean)
    tenure = Column(Integer)
    monthly_charges = Column(Float)
    total_charges = Column(Float)

class PhoneServiceModel(Base):
    __tablename__ = "phone_services"
    customer_id = Column(Text, primary_key=True)
    has_phone_service = Column(Boolean)
    multiple_lines = Column(Text)

class InternetServiceModel(Base):
    __tablename__ = "internet_services"
    customer_id = Column(Text, primary_key=True)
    internet_service = Column(Text)
    online_security = Column(Text)
    online_backup = Column(Text)
    device_protection = Column(Text)
    tech_support = Column(Text)
    streaming_tv = Column(Text)
    streaming_movies = Column(Text)

class BillingModel(Base):
    __tablename__ = "billing"
    customer_id = Column(Text, primary_key=True)
    contract_type = Column(Text)
    paperless_billing = Column(Boolean)
    payment_method = Column(Text)



# Pydantic Models for Request/Response
class CustomerCreate(BaseModel):
    customer_id: str
    gender: str
    is_senior_citizen: bool
    has_partner: bool
    has_dependents: bool
    tenure: int
    monthly_charges: float
    total_charges: float

class PhoneServiceCreate(BaseModel):
    customer_id: str
    has_phone_service: bool
    multiple_lines: str

class InternetServiceCreate(BaseModel):
    customer_id: str
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str

class BillingCreate(BaseModel):
    customer_id: str
    contract_type: str
    paperless_billing: bool
    payment_method: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for response
class GenderCount(BaseModel):
    gender: str
    count: int


# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the schema for the input data using Pydantic
class InputData(BaseModel):
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: int
    PhoneService: int
    MultipleLines: int
    InternetService: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    Contract: int
    PaperlessBilling: int
    PaymentMethod: int
    MonthlyCharges: float
    TotalCharges: float
    Churn: int

@app.post("/predict")
async def predict(data: InputData):
    try:
        input_df = pd.DataFrame([data.dict()])
        predictions = loaded_model.predict(input_df.drop(columns=["Churn"], errors="ignore"))
        return {"prediction": int(predictions[0])}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def root():
    return {"message": "API is running"}

# Customers CRUD
@app.post("/customers/", response_model=CustomerCreate)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = CustomerModel(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return customer

@app.get("/customers/", response_model=List[CustomerCreate])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(CustomerModel).offset(skip).limit(limit).all()
    return customers

@app.get("/customers/{customer_id}", response_model=CustomerCreate)
def read_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Similar CRUD endpoints for PhoneService, InternetService, Billing...
@app.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_customers = db.query(CustomerModel).count()
    senior_citizens = db.query(CustomerModel).filter(CustomerModel.is_senior_citizen == True).count()
    fiber_optic_users = db.query(InternetServiceModel).filter(InternetServiceModel.internet_service == 'Fiber optic').count()
    
    return {
        "total_customers": total_customers,
        "senior_citizens": senior_citizens,
        "fiber_optic_users": fiber_optic_users
    }

# Example Complex Query
@app.get("/customers/filter")
def filter_customers(
    gender: Optional[str] = None, 
    is_senior_citizen: Optional[bool] = None, 
    min_tenure: Optional[int] = None,
    max_tenure: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CustomerModel)
    
    if gender:
        query = query.filter(CustomerModel.gender == gender)
    
    if is_senior_citizen is not None:
        query = query.filter(CustomerModel.is_senior_citizen == is_senior_citizen)
    
    if min_tenure is not None:
        query = query.filter(CustomerModel.tenure >= min_tenure)
    
    if max_tenure is not None:
        query = query.filter(CustomerModel.tenure <= max_tenure)
    
    return query.all()


@app.get("/customer-demographics")
def get_customer_demographics(db: Session = Depends(get_db)):
    # Count customers with partners
    partners_count = db.query(CustomerModel).filter(CustomerModel.has_partner == True).count()
    
    # Count customers with dependents
    dependents_count = db.query(CustomerModel).filter(CustomerModel.has_dependents == True).count()
    
    # Count senior citizens
    senior_count = db.query(CustomerModel).filter(CustomerModel.is_senior_citizen == True).count()
    
    return [
        {"category": "has_partner", "count": partners_count, "fill": "hsl(var(--chart-1))"},
        {"category": "has_dependents", "count": dependents_count, "fill": "hsl(var(--chart-2))"},
        {"category": "is_senior", "count": senior_count, "fill": "hsl(var(--chart-3))"}
    ]



from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from pydantic import BaseModel

# Pydantic model for Internet Service
class InternetServiceBase(BaseModel):
    customer_id: str
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str

    class Config:
        from_attributes = True

# Extended model for creating new service entries
class InternetServiceCreate(InternetServiceBase):
    pass

# GET all internet services endpoint
@app.get("/internet-services/", response_model=List[InternetServiceBase])
def read_internet_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    services = db.query(InternetServiceModel).offset(skip).limit(limit).all()
    return services

# GET specific internet service by customer ID
@app.get("/internet-services/{customer_id}", response_model=InternetServiceBase)
def read_internet_service(customer_id: str, db: Session = Depends(get_db)):
    service = db.query(InternetServiceModel).filter(
        InternetServiceModel.customer_id == customer_id
    ).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Internet service not found")
    return service

# POST new internet service
@app.post("/internet-services/", response_model=InternetServiceBase)
def create_internet_service(
    service: InternetServiceCreate,
    db: Session = Depends(get_db)
):
    db_service = InternetServiceModel(**service.dict())
    db.add(db_service)
    try:
        db.commit()
        db.refresh(db_service)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_service

# PUT update internet service
@app.put("/internet-services/{customer_id}", response_model=InternetServiceBase)
def update_internet_service(
    customer_id: str,
    service: InternetServiceCreate,
    db: Session = Depends(get_db)
):
    db_service = db.query(InternetServiceModel).filter(
        InternetServiceModel.customer_id == customer_id
    ).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Internet service not found")
    
    for var, value in vars(service).items():
        setattr(db_service, var, value)
    
    try:
        db.commit()
        db.refresh(db_service)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_service

# DELETE internet service
@app.delete("/internet-services/{customer_id}")
def delete_internet_service(customer_id: str, db: Session = Depends(get_db)):
    service = db.query(InternetServiceModel).filter(
        InternetServiceModel.customer_id == customer_id
    ).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Internet service not found")
    
    try:
        db.delete(service)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Service deleted successfully"}

# GET filtered internet services
@app.get("/internet-services/filter/", response_model=List[InternetServiceBase])
def filter_internet_services(
    internet_service: Optional[str] = Query(None),
    online_security: Optional[str] = Query(None),
    tech_support: Optional[str] = Query(None),
    streaming_service: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(InternetServiceModel)
    
    if internet_service:
        query = query.filter(InternetServiceModel.internet_service == internet_service)
    
    if online_security:
        query = query.filter(InternetServiceModel.online_security == online_security)
    
    if tech_support:
        query = query.filter(InternetServiceModel.tech_support == tech_support)
    
    if streaming_service is not None:
        if streaming_service:
            query = query.filter(
                or_(
                    InternetServiceModel.streaming_tv == 'Yes',
                    InternetServiceModel.streaming_movies == 'Yes'
                )
            )
        else:
            query = query.filter(
                and_(
                    InternetServiceModel.streaming_tv == 'No',
                    InternetServiceModel.streaming_movies == 'No'
                )
            )
    
    return query.all()

# GET summary statistics
@app.get("/internet-services/summary/stats")
def get_internet_services_stats(db: Session = Depends(get_db)):
    total_services = db.query(InternetServiceModel).count()
    
    fiber_optic_count = db.query(InternetServiceModel).filter(
        InternetServiceModel.internet_service == 'Fiber optic'
    ).count()
    
    dsl_count = db.query(InternetServiceModel).filter(
        InternetServiceModel.internet_service == 'DSL'
    ).count()
    
    streaming_users = db.query(InternetServiceModel).filter(
        or_(
            InternetServiceModel.streaming_tv == 'Yes',
            InternetServiceModel.streaming_movies == 'Yes'
        )
    ).count()
    
    security_enabled = db.query(InternetServiceModel).filter(
        InternetServiceModel.online_security == 'Yes'
    ).count()
    
    return {
        "total_services": total_services,
        "fiber_optic_users": fiber_optic_count,
        "dsl_users": dsl_count,
        "streaming_users": streaming_users,
        "security_enabled_users": security_enabled,
        "fiber_optic_percentage": (fiber_optic_count / total_services * 100) if total_services > 0 else 0,
        "security_adoption_rate": (security_enabled / total_services * 100) if total_services > 0 else 0
    }


class PhoneServiceResponse(BaseModel):
    customer_id: str
    has_phone_service: bool
    multiple_lines: str

    class Config:
        orm_mode = True

@app.get("/phone-services/", response_model=List[PhoneServiceResponse])
def get_phone_services(db: Session = Depends(get_db)):
    services = db.query(PhoneServiceModel).all()
    return services




# Pydantic model for Billing
class BillingBase(BaseModel):
    customer_id: str
    contract_type: str
    paperless_billing: bool
    payment_method: str

    class Config:
        from_attributes = True

# GET all billing records
@app.get("/billing/", response_model=List[BillingBase])
def read_billing_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    records = db.query(BillingModel).offset(skip).limit(limit).all()
    return records

# GET billing record by customer ID
@app.get("/billing/{customer_id}", response_model=BillingBase)
def read_billing_record(customer_id: str, db: Session = Depends(get_db)):
    record = db.query(BillingModel).filter(
        BillingModel.customer_id == customer_id
    ).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return record

# POST new billing record
@app.post("/billing/", response_model=BillingBase)
def create_billing_record(
    record: BillingBase,
    db: Session = Depends(get_db)
):
    db_record = BillingModel(**record.dict())
    db.add(db_record)
    try:
        db.commit()
        db.refresh(db_record)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_record

# PUT update billing record
@app.put("/billing/{customer_id}", response_model=BillingBase)
def update_billing_record(
    customer_id: str,
    record: BillingBase,
    db: Session = Depends(get_db)
):
    db_record = db.query(BillingModel).filter(
        BillingModel.customer_id == customer_id
    ).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Billing record not found")
    
    for var, value in vars(record).items():
        setattr(db_record, var, value)
    
    try:
        db.commit()
        db.refresh(db_record)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_record

# DELETE billing record
@app.delete("/billing/{customer_id}")
def delete_billing_record(customer_id: str, db: Session = Depends(get_db)):
    record = db.query(BillingModel).filter(
        BillingModel.customer_id == customer_id
    ).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Billing record not found")
    
    try:
        db.delete(record)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Billing record deleted successfully"}

# GET billing summary statistics
@app.get("/billing/summary/stats")
def get_billing_stats(db: Session = Depends(get_db)):
    total_records = db.query(BillingModel).count()
    
    contract_breakdown = {
        "month_to_month": db.query(BillingModel).filter(
            BillingModel.contract_type == 'Month-to-month'
        ).count(),
        "one_year": db.query(BillingModel).filter(
            BillingModel.contract_type == 'One year'
        ).count(),
        "two_year": db.query(BillingModel).filter(
            BillingModel.contract_type == 'Two year'
        ).count()
    }
    
    paperless_billing_count = db.query(BillingModel).filter(
        BillingModel.paperless_billing == True
    ).count()
    
    payment_method_breakdown = {
        "electronic_check": db.query(BillingModel).filter(
            BillingModel.payment_method == 'Electronic check'
        ).count(),
        "mailed_check": db.query(BillingModel).filter(
            BillingModel.payment_method == 'Mailed check'
        ).count(),
        "bank_transfer": db.query(BillingModel).filter(
            BillingModel.payment_method == 'Bank transfer (automatic)'
        ).count(),
        "credit_card": db.query(BillingModel).filter(
            BillingModel.payment_method == 'Credit card (automatic)'
        ).count()
    }
    
    return {
        "total_records": total_records,
        "contract_breakdown": contract_breakdown,
        "paperless_billing_rate": (paperless_billing_count / total_records * 100) if total_records > 0 else 0,
        "payment_method_breakdown": payment_method_breakdown
    }


def execute_sql_query(db: Session, query: str) -> List[Dict[Any, Any]]:
    try:
        # print('sql_query:', query)
        result = db.execute(text(query))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

class ChatRequest(BaseModel):
    messages: list
    model: str 

# Pydantic models for request/response
class Message(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    content: str

# Initialize Groq client
groq_client = Groq(api_key="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")

# Chat endpoint using Groq SDK
SYSTEM_PROMPT = """You are an expert database analyst and AI assistant for a telecommunications customer database. You have access to the following PostgreSQL database schema:

-- Customers Table (Main Entity)
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    gender TEXT CHECK (gender IN ('Female', 'Male')),
    is_senior_citizen BOOLEAN,
    has_partner BOOLEAN,
    has_dependents BOOLEAN,
    tenure INTEGER,
    monthly_charges NUMERIC(10,2),
    total_charges NUMERIC(10,2)
);

-- Phone Service Table
CREATE TABLE phone_services (
    customer_id TEXT PRIMARY KEY,
    has_phone_service BOOLEAN,
    multiple_lines TEXT CHECK (multiple_lines IN ('No phone service', 'No', 'Yes')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Internet Service Table
CREATE TABLE internet_services (
    customer_id TEXT PRIMARY KEY,
    internet_service TEXT CHECK (internet_service IN ('DSL', 'Fiber optic', 'No')),
    online_security TEXT CHECK (online_security IN ('No', 'Yes', 'No internet service')),
    online_backup TEXT CHECK (online_backup IN ('No', 'Yes', 'No internet service')),
    device_protection TEXT CHECK (device_protection IN ('No', 'Yes', 'No internet service')),
    tech_support TEXT CHECK (tech_support IN ('No', 'Yes', 'No internet service')),
    streaming_tv TEXT CHECK (streaming_tv IN ('No', 'Yes', 'No internet service')),
    streaming_movies TEXT CHECK (streaming_movies IN ('No', 'Yes', 'No internet service')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Billing Table
CREATE TABLE billing (
    customer_id TEXT PRIMARY KEY,
    contract_type TEXT CHECK (contract_type IN ('Month-to-month', 'One year', 'Two year')),
    paperless_billing BOOLEAN,
    payment_method TEXT CHECK (payment_method IN ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

Important Guidelines:

1. Generate PostgreSQL queries that answer the user's question precisely
2. Always use safe practices and parameterized queries
3. Join tables appropriately when needed
4. Consider performance and use appropriate aggregations
5. Provide clear explanations of your queries and results

Format your response as:
SQL_QUERY: <the SQL query>
EXPLANATION: <explanation of what you're querying>
"""

@app.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Prepare messages, including the system prompt
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + request.messages

        # Use the model passed from the frontend
        model = request.model

        # Step 1: Get SQL query from LLM using the dynamically selected model
        chat_completion = groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_tokens=1024,
        )

        response_content = chat_completion.choices[0].message.content
        print('LLM Response:', response_content)

        # Enhanced parsing of the response to extract SQL query
        sql_match = re.search(r'SQL_QUERY:\s*(.+?)(?=EXPLANATION:|$)', response_content, re.DOTALL)
        
        if sql_match:
            sql_query = sql_match.group(1).strip()

            # Clean the SQL query for database execution (no second LLM request needed)
            clean_sql_query = sql_query
            print('Cleaned SQL Query1:', clean_sql_query)

            # Return just the cleaned SQL query
            return {
                "cleaned_sql_query": clean_sql_query
            }
        
        return {
            "error": "Could not extract SQL query from the response",
            "llm_response": response_content
        }

    except Exception as e:
        print(f"Unexpected error in chat endpoint: {str(e)}")
        return {
            "error": f"Unexpected server error: {str(e)}"
        }





@app.get("/api/status")
async def get_status():
    # This will return a JSON response with status and message
    return JSONResponse(content={"status": "ok", "message": "Chat API is working"})
