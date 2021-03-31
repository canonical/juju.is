from base64 import b64encode


def _get_metadata(job, name):
    metadata_map = {
        "description": 2739137,
    }

    for data in job["metadata"]:
        if data["id"] == metadata_map[name]:
            return data["value"]
    return None


class Vacancy:
    def __init__(self, job: dict):
        self.id: str = job["id"]
        self.title: str = job["title"]
        self.department: str = job["departments"][0]["name"]
        self.description: str = _get_metadata(job, "description")


class Greenhouse:
    def __init__(
        self,
        session,
        api_key,
        base_url="https://boards-api.greenhouse.io/v1/boards/Canonical/jobs",
    ):
        self.session = session
        self.base64_key = b64encode(f"{api_key}:".encode()).decode()
        self.base_url = base_url

    """
    Get all jobs from the API and parse them into vacancies
    Filter out vacancies without an office and a department
    """

    def get_vacancies(self):
        feed = self.session.get(f"{self.base_url}?content=true").json()

        vacancies = []

        for job in feed["jobs"]:
            vacancies.append(Vacancy(job))

        return vacancies

    """
    Get vacancies where the department matches a given department
    """

    def get_vacancies_by_department_slug(self, department):
        vacancies = self.get_vacancies()

        def department_filter(vacancy):
            return vacancy.department == department

        return list(filter(department_filter, vacancies))
