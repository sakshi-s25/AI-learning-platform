from app.database import SessionLocal, Base, engine
from app.models.competency import Competency
from app.models.question import Question
from app.models.course import Course
from app.models import user  # noqa: F401 — registers the users table

COMPETENCIES = [
    ("Statistical Methods", "Analytical"),
    ("Data Collection", "Field Operations"),
    ("Data Cleaning", "Analytical"),
    ("Data Visualization", "Analytical"),
    ("Survey Methodology", "Field Operations"),
    ("Sampling", "Analytical"),
    ("Statistical Computing", "Technical"),
    ("Data Interpretation", "Analytical"),
    ("Data Quality", "Governance"),
    ("Official Statistics Concepts", "Governance"),
]

# (competency_name, question_text, options, correct_option_index, explanation)
QUESTIONS = [
    ("Statistical Methods",
     "Which measure of central tendency is most affected by extreme outliers?",
     ["Median", "Mean", "Mode", "Range"], 1,
     "The mean is pulled toward extreme values, while the median stays stable."),
    ("Statistical Methods",
     "A p-value of 0.03 at the 5% significance level typically leads to which conclusion?",
     ["Increase the sample size", "No conclusion can be drawn", "Reject the null hypothesis", "Accept the null hypothesis outright"], 2,
     "0.03 is below the 0.05 threshold, so the null hypothesis is rejected."),

    ("Data Collection",
     "Which data collection method typically yields the highest response accuracy for sensitive topics?",
     ["Face-to-face interview by a known official", "Telephone interview", "Group discussion", "Self-administered anonymous questionnaire"], 3,
     "Anonymity reduces social-desirability bias on sensitive questions."),
    ("Data Collection",
     "What is a key disadvantage of using secondary data sources for statistical analysis?",
     ["Data may not exactly match the current research objective", "It is always more expensive", "It cannot be verified at all", "It requires no data cleaning"], 0,
     "Secondary data was collected for a different purpose, so it may not fit the new objective precisely."),

    ("Data Cleaning",
     "What is the recommended first step when handling missing values in a large dataset?",
     ["Delete all rows with missing values", "Understand the pattern/reason for missingness", "Replace all missing values with zero", "Ignore missing values"], 1,
     "Understanding why data is missing determines the right handling strategy."),
    ("Data Cleaning",
     "Which technique helps identify outliers in a numeric column?",
     ["Sorting alphabetically", "Counting unique values only", "Interquartile Range (IQR) method", "Checking column data type only"], 2,
     "The IQR method flags values far outside the typical spread of the data."),

    ("Data Visualization",
     "Which chart type is most appropriate for showing a trend over multiple years?",
     ["Pie chart", "Scatter plot without axes", "Word cloud", "Line chart"], 3,
     "Line charts are built to show change over a continuous axis like time."),
    ("Data Visualization",
     "What is a common pitfall when creating bar charts for comparison?",
     ["Starting the y-axis at a value other than zero, exaggerating differences", "Using consistent bar widths", "Labeling the axes clearly", "Using a single color for the same category"], 0,
     "A truncated y-axis can make small differences look much larger than they are."),

    ("Survey Methodology",
     "What does 'non-response bias' refer to in a survey?",
     ["Random errors in data entry", "Systematic differences between respondents and non-respondents that skew results", "The cost of conducting the survey", "The length of the questionnaire"], 1,
     "If those who don't respond differ systematically from those who do, results are skewed."),
    ("Survey Methodology",
     "Pilot testing a questionnaire before full deployment mainly helps to:",
     ["Increase the sample size automatically", "Replace the need for sampling", "Identify unclear or problematic questions before wide rollout", "Guarantee a 100% response rate"], 2,
     "Pilots surface confusing wording or design issues before the real rollout."),

    ("Sampling",
     "In stratified sampling, the population is first divided into:",
     ["Random unordered clusters only", "A single large group", "Equal-sized geographic zones only", "Homogeneous subgroups (strata) before sampling within each"], 3,
     "Stratification groups similar units together, then samples within each stratum."),
    ("Sampling",
     "What is the main advantage of probability sampling over non-probability sampling?",
     ["It allows calculation of sampling error and generalization to the population", "It is always faster to conduct", "It requires no sampling frame", "It eliminates all bias automatically"], 0,
     "Known selection probabilities let you estimate error and generalize results."),

    ("Statistical Computing",
     "Which of the following is commonly used in Python for numerical/array computations?",
     ["HTML", "NumPy", "CSS", "FTP"], 1,
     "NumPy is the standard Python library for numerical array operations."),
    ("Statistical Computing",
     "What is the main purpose of using version control (e.g., Git) in a statistical workflow?",
     ["Encrypt survey responses", "Visualize data automatically", "Track changes to code/analysis and collaborate safely", "Clean missing values automatically"], 2,
     "Version control tracks who changed what, and lets teams collaborate without overwriting each other."),

    ("Data Interpretation",
     "Correlation between two variables implies:",
     ["Definite causation", "No relationship at all", "That the variables are identical", "An association, but not necessarily that one causes the other"], 3,
     "Correlation shows a relationship exists, not that one variable causes the other."),
    ("Data Interpretation",
     "When interpreting a result with a wide confidence interval, one should:",
     ["Be cautious, as the estimate is less precise", "Treat it as highly precise", "Ignore the confidence interval entirely", "Assume the sample size was very large"], 0,
     "A wide interval signals more uncertainty around the estimate."),

    ("Data Quality",
     "Which of these is NOT typically considered a dimension of data quality?",
     ["Accuracy", "Color scheme of the report", "Completeness", "Timeliness"], 1,
     "Report styling isn't a data quality dimension; accuracy, completeness, and timeliness are."),
    ("Data Quality",
     "Data validation rules (e.g., 'age must be between 0 and 120') are primarily used to:",
     ["Automatically generate charts", "Replace the need for sampling", "Catch implausible or erroneous entries at the point of data entry", "Increase survey response rates"], 2,
     "Validation rules flag impossible values as they're entered, before they pollute the dataset."),

    ("Official Statistics Concepts",
     "In official statistics, what does 'metadata' refer to?",
     ["The final published statistic only", "Personal data of respondents", "A type of survey question", "Data that describes other data, such as definitions and methodology"], 3,
     "Metadata explains how a statistic was defined and produced, not the statistic itself."),
    ("Official Statistics Concepts",
     "Why is methodological transparency important in official statistics?",
     ["It allows users to understand and trust how the figures were produced", "It is required only for internal use", "It replaces the need for data quality checks", "It has no effect on public trust"], 0,
     "Publishing methodology lets users judge how much to trust and how to use the figures."),
]

COURSES = [
    ("Statistical Methods", "Foundations of Statistical Inference",
     "Core concepts: mean, median, hypothesis testing, and when to use each.", "Beginner"),
    ("Statistical Methods", "Hypothesis Testing in Practice",
     "Applying significance tests to real official-statistics scenarios.", "Intermediate"),

    ("Data Collection", "Field Data Collection Essentials",
     "Best practices for accurate, low-bias data collection in the field.", "Beginner"),
    ("Data Collection", "Designing Reliable Data Collection Instruments",
     "How to build questionnaires and forms that minimize error.", "Intermediate"),

    ("Data Cleaning", "Data Cleaning Fundamentals",
     "Spotting and fixing common data entry and formatting issues.", "Beginner"),
    ("Data Cleaning", "Handling Missing and Outlier Data",
     "Strategies for missing values and outliers without distorting results.", "Intermediate"),

    ("Data Visualization", "Effective Charts for Official Statistics",
     "Choosing the right chart type for the story your data tells.", "Beginner"),
    ("Data Visualization", "Avoiding Misleading Visualizations",
     "Common chart pitfalls that unintentionally mislead readers.", "Intermediate"),

    ("Survey Methodology", "Survey Design Basics",
     "Structuring a survey from objective to final questionnaire.", "Beginner"),
    ("Survey Methodology", "Reducing Non-Response and Bias",
     "Techniques to improve response rates and representative data.", "Intermediate"),

    ("Sampling", "Sampling Fundamentals",
     "Why we sample, and the difference between probability and non-probability methods.", "Beginner"),
    ("Sampling", "Stratified and Probability Sampling",
     "Designing stratified samples for more precise estimates.", "Intermediate"),

    ("Statistical Computing", "Python for Statistical Computing",
     "Using Python and NumPy/Pandas for statistical analysis.", "Beginner"),
    ("Statistical Computing", "Version Control for Data Teams",
     "Using Git to track analysis code and collaborate safely.", "Intermediate"),

    ("Data Interpretation", "Interpreting Statistical Results Correctly",
     "Reading results without overstating what the numbers show.", "Beginner"),
    ("Data Interpretation", "Correlation, Causation, and Confidence Intervals",
     "Avoiding common interpretation mistakes in official reporting.", "Intermediate"),

    ("Data Quality", "Data Quality Dimensions Explained",
     "Accuracy, completeness, timeliness, and why each matters.", "Beginner"),
    ("Data Quality", "Building Data Validation Rules",
     "Designing rules that catch bad data before it spreads.", "Intermediate"),

    ("Official Statistics Concepts", "Introduction to Official Statistics",
     "What makes a statistic 'official', and core governance principles.", "Beginner"),
    ("Official Statistics Concepts", "Metadata and Methodological Transparency",
     "Why publishing methodology builds public trust in statistics.", "Intermediate"),
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        name_to_competency = {}
        for name, category in COMPETENCIES:
            existing = db.query(Competency).filter(Competency.name == name).first()
            if not existing:
                existing = Competency(name=name, category=category, required_level=75.0)
                db.add(existing)
                db.flush()  # assigns an id without committing yet
            name_to_competency[name] = existing

        added = 0
        for comp_name, question_text, options, correct_index, explanation in QUESTIONS:
            already_exists = (
                db.query(Question).filter(Question.question_text == question_text).first()
            )
            if already_exists:
                continue
            db.add(
                Question(
                    competency_id=name_to_competency[comp_name].id,
                    question_text=question_text,
                    options=options,
                    correct_option_index=correct_index,
                    explanation=explanation,
                    difficulty="Medium",
                    is_ai_generated=False,
                )
            )
            added += 1

        db.commit()
        print(f"Seeded {len(COMPETENCIES)} competencies and {added} new questions.")

        courses_added = 0
        for comp_name, title, description, difficulty in COURSES:
            already_exists = db.query(Course).filter(Course.title == title).first()
            if already_exists:
                continue
            db.add(
                Course(
                    title=title,
                    competency_id=name_to_competency[comp_name].id,
                    description=description,
                    resource_url="#",
                    difficulty=difficulty,
                )
            )
            courses_added += 1

        db.commit()
        print(f"Seeded {courses_added} new courses.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
