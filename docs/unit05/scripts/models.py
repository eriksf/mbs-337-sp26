from pydantic import BaseModel

class ReadSummary(BaseModel):
    id: str
    sequence: str
    total_bases: int
    average_phred: float

class FastqSummary(BaseModel):
    reads: list[ReadSummary]
