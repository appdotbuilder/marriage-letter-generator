from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum


class MaritalStatus(str, Enum):
    SINGLE = "single"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class EducationLevel(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DIPLOMA = "diploma"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORATE = "doctorate"
    PROFESSIONAL = "professional"


class Religion(str, Enum):
    ISLAM = "islam"
    CHRISTIANITY = "christianity"
    HINDUISM = "hinduism"
    BUDDHISM = "buddhism"
    JUDAISM = "judaism"
    OTHER = "other"


class LetterType(str, Enum):
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"
    N4 = "N4"
    N5 = "N5"


# Persistent models (stored in database)
class Person(SQLModel, table=True):
    """Base person model for husband, wife, and parents"""

    __tablename__ = "persons"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=255)
    date_of_birth: date
    place_of_birth: str = Field(max_length=255)
    nationality: str = Field(max_length=100)
    religion: Religion
    occupation: str = Field(max_length=255)
    education_level: EducationLevel
    institution_name: str = Field(default="", max_length=255)
    graduation_year: Optional[int] = Field(default=None)
    monthly_income: Optional[Decimal] = Field(default=None, decimal_places=2)
    address: str = Field(max_length=500)
    phone_number: str = Field(max_length=20)
    email: str = Field(default="", max_length=255)
    height_cm: Optional[int] = Field(default=None)
    weight_kg: Optional[Decimal] = Field(default=None, decimal_places=1)
    complexion: str = Field(default="", max_length=100)
    physical_disabilities: str = Field(default="", max_length=500)
    health_conditions: str = Field(default="", max_length=500)
    hobbies: str = Field(default="", max_length=500)
    additional_notes: str = Field(default="", max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    as_husband_letters: List["MarriageLetter"] = Relationship(
        back_populates="husband", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_id]"}
    )
    as_wife_letters: List["MarriageLetter"] = Relationship(
        back_populates="wife", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_id]"}
    )
    as_husband_father_letters: List["MarriageLetter"] = Relationship(
        back_populates="husband_father", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_father_id]"}
    )
    as_husband_mother_letters: List["MarriageLetter"] = Relationship(
        back_populates="husband_mother", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_mother_id]"}
    )
    as_wife_father_letters: List["MarriageLetter"] = Relationship(
        back_populates="wife_father", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_father_id]"}
    )
    as_wife_mother_letters: List["MarriageLetter"] = Relationship(
        back_populates="wife_mother", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_mother_id]"}
    )


class MarriagePreferences(SQLModel, table=True):
    """Preferences for marriage partner"""

    __tablename__ = "marriage_preferences"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    preferred_age_min: Optional[int] = Field(default=None)
    preferred_age_max: Optional[int] = Field(default=None)
    preferred_education: Optional[EducationLevel] = Field(default=None)
    preferred_occupation: str = Field(default="", max_length=255)
    preferred_religion: Optional[Religion] = Field(default=None)
    preferred_nationality: str = Field(default="", max_length=100)
    preferred_location: str = Field(default="", max_length=255)
    preferred_income_min: Optional[Decimal] = Field(default=None, decimal_places=2)
    preferred_height_min: Optional[int] = Field(default=None)
    preferred_height_max: Optional[int] = Field(default=None)
    marital_status_acceptable: List[str] = Field(default=[], sa_column=Column(JSON))
    additional_requirements: str = Field(default="", max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    husband_preferences: List["MarriageLetter"] = Relationship(
        back_populates="husband_preferences_obj",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_preferences_id]"},
    )
    wife_preferences: List["MarriageLetter"] = Relationship(
        back_populates="wife_preferences_obj",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_preferences_id]"},
    )


class FamilyBackground(SQLModel, table=True):
    """Family background information"""

    __tablename__ = "family_backgrounds"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    family_origin: str = Field(max_length=255)
    ancestral_home: str = Field(max_length=255)
    family_traditions: str = Field(default="", max_length=1000)
    social_status: str = Field(default="", max_length=255)
    family_values: str = Field(default="", max_length=1000)
    number_of_siblings: int = Field(default=0)
    siblings_details: str = Field(default="", max_length=1000)
    family_income_range: str = Field(default="", max_length=100)
    property_details: str = Field(default="", max_length=500)
    family_reputation: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    husband_families: List["MarriageLetter"] = Relationship(
        back_populates="husband_family", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_family_id]"}
    )
    wife_families: List["MarriageLetter"] = Relationship(
        back_populates="wife_family", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_family_id]"}
    )


class MarriageLetter(SQLModel, table=True):
    """Main marriage letter containing all biodata"""

    __tablename__ = "marriage_letters"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    letter_type: LetterType
    reference_number: str = Field(unique=True, max_length=50)

    # Husband information
    husband_id: int = Field(foreign_key="persons.id")
    husband_father_id: Optional[int] = Field(default=None, foreign_key="persons.id")
    husband_mother_id: Optional[int] = Field(default=None, foreign_key="persons.id")
    husband_marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    husband_family_id: Optional[int] = Field(default=None, foreign_key="family_backgrounds.id")
    husband_preferences_id: Optional[int] = Field(default=None, foreign_key="marriage_preferences.id")

    # Wife information
    wife_id: int = Field(foreign_key="persons.id")
    wife_father_id: Optional[int] = Field(default=None, foreign_key="persons.id")
    wife_mother_id: Optional[int] = Field(default=None, foreign_key="persons.id")
    wife_marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    wife_family_id: Optional[int] = Field(default=None, foreign_key="family_backgrounds.id")
    wife_preferences_id: Optional[int] = Field(default=None, foreign_key="marriage_preferences.id")

    # Letter metadata
    purpose: str = Field(max_length=500)
    special_requests: str = Field(default="", max_length=1000)
    contact_person: str = Field(max_length=255)
    contact_phone: str = Field(max_length=20)
    contact_email: str = Field(default="", max_length=255)

    # Status and timestamps
    is_printed: bool = Field(default=False)
    print_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Custom fields for specific letter types
    custom_fields: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # Relationships
    husband: Person = Relationship(
        back_populates="as_husband_letters", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_id]"}
    )
    wife: Person = Relationship(
        back_populates="as_wife_letters", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_id]"}
    )
    husband_father: Optional[Person] = Relationship(
        back_populates="as_husband_father_letters",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_father_id]"},
    )
    husband_mother: Optional[Person] = Relationship(
        back_populates="as_husband_mother_letters",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_mother_id]"},
    )
    wife_father: Optional[Person] = Relationship(
        back_populates="as_wife_father_letters",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_father_id]"},
    )
    wife_mother: Optional[Person] = Relationship(
        back_populates="as_wife_mother_letters",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_mother_id]"},
    )
    husband_family: Optional[FamilyBackground] = Relationship(
        back_populates="husband_families", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_family_id]"}
    )
    wife_family: Optional[FamilyBackground] = Relationship(
        back_populates="wife_families", sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_family_id]"}
    )
    husband_preferences_obj: Optional[MarriagePreferences] = Relationship(
        back_populates="husband_preferences",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.husband_preferences_id]"},
    )
    wife_preferences_obj: Optional[MarriagePreferences] = Relationship(
        back_populates="wife_preferences",
        sa_relationship_kwargs={"foreign_keys": "[MarriageLetter.wife_preferences_id]"},
    )


# Non-persistent schemas (for validation, forms, API requests/responses)
class PersonCreate(SQLModel, table=False):
    """Schema for creating a person"""

    full_name: str = Field(max_length=255)
    date_of_birth: date
    place_of_birth: str = Field(max_length=255)
    nationality: str = Field(max_length=100)
    religion: Religion
    occupation: str = Field(max_length=255)
    education_level: EducationLevel
    institution_name: str = Field(default="", max_length=255)
    graduation_year: Optional[int] = Field(default=None)
    monthly_income: Optional[Decimal] = Field(default=None, decimal_places=2)
    address: str = Field(max_length=500)
    phone_number: str = Field(max_length=20)
    email: str = Field(default="", max_length=255)
    height_cm: Optional[int] = Field(default=None)
    weight_kg: Optional[Decimal] = Field(default=None, decimal_places=1)
    complexion: str = Field(default="", max_length=100)
    physical_disabilities: str = Field(default="", max_length=500)
    health_conditions: str = Field(default="", max_length=500)
    hobbies: str = Field(default="", max_length=500)
    additional_notes: str = Field(default="", max_length=1000)


class MarriagePreferencesCreate(SQLModel, table=False):
    """Schema for creating marriage preferences"""

    preferred_age_min: Optional[int] = Field(default=None)
    preferred_age_max: Optional[int] = Field(default=None)
    preferred_education: Optional[EducationLevel] = Field(default=None)
    preferred_occupation: str = Field(default="", max_length=255)
    preferred_religion: Optional[Religion] = Field(default=None)
    preferred_nationality: str = Field(default="", max_length=100)
    preferred_location: str = Field(default="", max_length=255)
    preferred_income_min: Optional[Decimal] = Field(default=None, decimal_places=2)
    preferred_height_min: Optional[int] = Field(default=None)
    preferred_height_max: Optional[int] = Field(default=None)
    marital_status_acceptable: List[str] = Field(default=[])
    additional_requirements: str = Field(default="", max_length=1000)


class FamilyBackgroundCreate(SQLModel, table=False):
    """Schema for creating family background"""

    family_origin: str = Field(max_length=255)
    ancestral_home: str = Field(max_length=255)
    family_traditions: str = Field(default="", max_length=1000)
    social_status: str = Field(default="", max_length=255)
    family_values: str = Field(default="", max_length=1000)
    number_of_siblings: int = Field(default=0)
    siblings_details: str = Field(default="", max_length=1000)
    family_income_range: str = Field(default="", max_length=100)
    property_details: str = Field(default="", max_length=500)
    family_reputation: str = Field(default="", max_length=500)


class MarriageLetterCreate(SQLModel, table=False):
    """Schema for creating a marriage letter"""

    letter_type: LetterType

    # Husband information
    husband_data: PersonCreate
    husband_father_data: Optional[PersonCreate] = Field(default=None)
    husband_mother_data: Optional[PersonCreate] = Field(default=None)
    husband_marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    husband_family_data: Optional[FamilyBackgroundCreate] = Field(default=None)
    husband_preferences_data: Optional[MarriagePreferencesCreate] = Field(default=None)

    # Wife information
    wife_data: PersonCreate
    wife_father_data: Optional[PersonCreate] = Field(default=None)
    wife_mother_data: Optional[PersonCreate] = Field(default=None)
    wife_marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    wife_family_data: Optional[FamilyBackgroundCreate] = Field(default=None)
    wife_preferences_data: Optional[MarriagePreferencesCreate] = Field(default=None)

    # Letter metadata
    purpose: str = Field(max_length=500)
    special_requests: str = Field(default="", max_length=1000)
    contact_person: str = Field(max_length=255)
    contact_phone: str = Field(max_length=20)
    contact_email: str = Field(default="", max_length=255)

    # Custom fields for specific letter types
    custom_fields: Dict[str, Any] = Field(default={})


class MarriageLetterResponse(SQLModel, table=False):
    """Schema for marriage letter response"""

    id: int
    letter_type: LetterType
    reference_number: str
    purpose: str
    contact_person: str
    contact_phone: str
    contact_email: str
    is_printed: bool
    print_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Include basic person information
    husband_name: str
    wife_name: str


class LetterPrintRequest(SQLModel, table=False):
    """Schema for printing a letter"""

    letter_id: int
    print_format: str = Field(default="pdf", max_length=10)
    include_photos: bool = Field(default=False)
    letterhead: str = Field(default="", max_length=255)
    additional_notes: str = Field(default="", max_length=500)


class LetterSummary(SQLModel, table=False):
    """Summary schema for letter listing"""

    id: int
    letter_type: LetterType
    reference_number: str
    husband_name: str
    wife_name: str
    created_at: datetime
    is_printed: bool
