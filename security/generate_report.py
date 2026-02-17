import logging

# Set up basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def generate_report(data):
    try:
        # Example report generation logic
        report = f"Report summary: {len(data)} items processed."
        logging.info("Report generated successfully")
        return report
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")
        return None


def save_report(report, filename="report.txt"):
    try:
        with open(filename, "w") as f:
            f.write(report)
        logging.info(f"Report saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save report to {filename}: {e}")
