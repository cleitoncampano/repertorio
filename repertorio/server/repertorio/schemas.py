from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Search(Model):
    query: str = Field(default='', max_length=500)
    kind: str = ''
    intention: str = ''
    technique: str = ''
    operation: str = ''
    movement: str = ''
    aesthetic: str = ''
    origin: str = ''
    format: str = ''
    min_strength: int = Field(default=0, ge=0, le=5)
    reusable: bool = False
    state: Literal['published', 'pending', 'trashed'] = 'published'
    limit: int = Field(default=24, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
    context_id: str | None = None


class AgentSearch(Search):
    limit: int = Field(default=16, ge=1, le=200)
    per_group: int = Field(default=1, ge=1, le=50)
    contact_sheet: bool = True


class Sheet(Model):
    ids: list[str] = Field(min_length=1, max_length=24)


class StartContext(Model):
    project_id: str
    demand: str = Field(min_length=3, max_length=3000)


class Project(Model):
    name: str = Field(min_length=1, max_length=120)
    root: str


class ReferenceData(Model):
    title: str = Field(min_length=1, max_length=240)
    description: str = Field(min_length=1, max_length=6000)
    idea: str = Field(min_length=1, max_length=6000)
    techniques: list[str] = Field(default_factory=list, max_length=10)
    intentions: list[str] = Field(default_factory=list, max_length=5)
    movements: list[str] = Field(default_factory=list, max_length=5)
    aesthetics: list[str] = Field(default_factory=list, max_length=8)
    strength: int = Field(default=3, ge=1, le=5)
    reusable: bool | None = None
    source_reference_ids: list[str] = Field(default_factory=list, max_length=40)
    usage_notes: str = Field(default='', max_length=3000)


class Register(Model):
    context_id: str
    request_key: str = Field(min_length=6, max_length=180)
    data: ReferenceData
    files: list[str] = Field(min_length=1, max_length=60)
    previews: list[str] = Field(default_factory=list, max_length=60)
    user_requested: bool = False


class Update(Model):
    context_id: str
    expected_revision: int = Field(ge=1)
    data: ReferenceData


class StateChange(Model):
    expected_revision: int = Field(ge=1)
    state: Literal['published', 'pending', 'trashed']
    context_id: str | None = None
    user_requested: bool = False


class Pack(Model):
    context_id: str
    title: str = Field(min_length=1, max_length=240)
    reference_ids: list[str] = Field(min_length=1, max_length=30)
    rationale: str = Field(default='', max_length=6000)
