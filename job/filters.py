import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    """
    JobFilter enables dynamic filtering of job listings based on various criteria.

    This filter allows users to search for jobs by title, publication date, company name,
    job type, and job level. Each filter field is described below:

    - title: A case-insensitive search for job titles that contain the specified keyword.
    - published_date: Filters jobs by their publication date.
    - company: A case-insensitive search for company names that contain the specified keyword.
    - job_type: Filters jobs by the type of job (e.g., Full-time, Part-time, Contract).
    - job_level: Filters jobs by the level of seniority (e.g., Junior, Mid, Senior).

    Parameters:
    -----------
    None (filters are applied via query parameters in the URL).

    Example:
    --------
    To filter jobs, you can use query parameters in your request URL, like so:
    /jobs/?title=developer&published_date=2023-07-01&company=TechCorp&job_type=FT&job_level=SR

    This example filters jobs that:
    - Contain the word "developer" in the title.
    - Were published on July 1, 2023.
    - Are posted by a company with "TechCorp" in its name.
    - Are full-time positions.
    - Are senior-level jobs.

    Returns:
    --------
    Filtered queryset of Job objects based on the applied filters.
    """

    title = django_filters.CharFilter(lookup_expr="icontains")
    published_date = django_filters.DateFilter()
    company = django_filters.CharFilter(lookup_expr="icontains")
    job_type = django_filters.ChoiceFilter(choices=Job.Job_type)
    job_level = django_filters.ChoiceFilter(choices=Job.SENIORITY_LEVEL)

    class Meta:
        model = Job
        fields = ["title", "published_date", "company", "job_type", "job_level"]
