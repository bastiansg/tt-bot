import regex

from typing import Optional


TEXT_NORM_PATTERN = regex.compile(r"\s{2,}")


def text_normalize(summary: Optional[str]) -> Optional[str]:
    if summary is None:
        return

    summary = summary.replace("\n", " ")
    summary = TEXT_NORM_PATTERN.sub(" ", summary)
    summary = summary.strip()

    return summary


def parse_education(education_item: dict) -> dict:
    time_period = education_item.get("timePeriod", {})
    parsed_education = {
        "school_name": education_item["schoolName"],
        "field_of_study": education_item.get("fieldOfStudy"),
        "start_year": time_period.get("startDate", {}).get("year"),
        "end_year": time_period.get("endDate", {}).get("year"),
    }

    return parsed_education


def parse_experience(experience_item: dict) -> dict:
    time_period = experience_item.get("timePeriod", {})
    parsed_experience = {
        "company_name": experience_item["companyName"],
        "title": experience_item.get("title"),
        "start_year": time_period.get("startDate", {}).get("year"),
        "end_year": time_period.get("endDate", {}).get("year"),
    }

    return parsed_experience


def parse_language(language_item: dict) -> dict:
    parsed_language = {
        "name": language_item["name"],
        "level": language_item.get("proficiency"),
    }

    return parsed_language


def parse_person_profile(person_profile: dict) -> str:
    name = (
        f"{person_profile.get('firstName')}"
        f" {person_profile.get('lastName')}"
    )

    experience = [
        parse_experience(experience_item)
        for experience_item in person_profile.get("experience", [])
    ]

    education = [
        parse_education(education_item)
        for education_item in person_profile.get("education", [])
    ]

    languages = [
        parse_language(language_item)
        for language_item in person_profile.get("languages", [])
    ]

    parsed_profile = {
        "linkedin_user_profile": {
            "name": name,
            "head_line": person_profile.get("headline"),
            "summary": text_normalize(person_profile.get("summary")),
            "industry_name": person_profile.get("industryName"),
            "experience": experience,
            "education": education,
            "languages": languages,
        }
    }

    return parsed_profile


def parse_company_profile(company_profile: dict) -> dict:
    industries = [
        industry["localizedName"]
        for industry in company_profile.get("companyIndustries", [])
    ]

    parsed_company_profile = {
        "linkedin_company_profile": {
            "name": company_profile["name"],
            "description": text_normalize(company_profile.get("description")),
            "industries": industries,
        }
    }

    return parsed_company_profile
