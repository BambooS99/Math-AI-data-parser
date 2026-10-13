import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from anthropic import Anthropic
from api import schemas
from api.services import problem_router

load_dotenv()
client = Anthropic()


CLASSIFIER_INSTRUCTIONS = """
Classify the user's message as one of the following operations:
- addition
- subtraction
- multiplication
- division
- mixed_expression
- derivative
- integral

Do not calculate or solve anything.

For arithmetic problems (addition, subtraction, multiplication, division):
- Extract only numeric operands into 'normalized_input', preserving their original order.

For mixed arithmetic expressions:
- Set 'problem_type' to 'mixed_expression'.
- Extract the complete numeric expression into 'expression', preserving operators and parentheses.
- The expression may combine addition, subtraction, multiplication, division, and exponents, but must not contain variables.

For calculus problems (derivative, integral):
- Set 'problem_type' to 'derivative' or 'integral'.
- Extract the normalized mathematical expression into 'expression' (e.g., '3*x^2 + 2*x', 'sin(x)', 'e^x').
- Extract the variable of differentiation or integration into 'variable' (defaults to 'x').
- For definite integrals, extract 'lower_bound' and 'upper_bound' if specified.

The 'expression' field must contain ONLY a math formula in one variable (e.g. '3*x^2 + 2*x'), never words or sentences.
Word problems, area/volume between curves, equations with several variables, limits, and anything that needs more than
one derivative or integral step are NOT supported: classify them as "unknown" with needs_clarification true.

If the message is unclear, combines incompatible operations, or is not one of these supported operations, use:
- problem_type: "unknown"
- normalized_input: []
- needs_clarification: true

Return only the fields required by the provided schema.
"""

app = FastAPI(title = "RAG API", version="1.0.0")

# Re-export route_problem for convenience and backwards compatibility
route_problem = problem_router.route_problem



# Comma-separated list of allowed frontend origins, e.g.
# FRONTEND_ORIGIN="https://yoursite.netlify.app,http://localhost:5173"
FRONTEND_ORIGINS = [
    o.strip().rstrip("/")
    for o in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: schemas.ChatRequest) -> schemas.ChatResponse:
    message= req.message
    classification = classify_problem(message)
    solver = problem_router.route_problem(classification)

    return schemas.ChatResponse(
        message = message,
        classification = classification,
        solver = solver,
    )

#functions

"""classification function"""
def classify_problem(message: str) -> schemas.ClassificationResult:
    response = client.messages.parse(
        model = "claude-haiku-4-5",
        max_tokens=256,
        system=CLASSIFIER_INSTRUCTIONS,
        messages=[{"role": "user", "content": message}],
        output_format=schemas.ClassificationResult,
    )
    return response.parsed_output






@app.get("/")

def read_root():
    return {"message": "welcome to the application"}