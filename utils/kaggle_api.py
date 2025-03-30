import re
import subprocess

def fetch_leaderboard_data(competition_name):
    """Fetch and parse leaderboard data from Kaggle API."""
    try:
        # Run the Kaggle API command
        result = subprocess.run(
            ["kaggle", "competitions", "leaderboard", "-c", competition_name, "--show"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode != 0:
            raise Exception(result.stderr)

        # Debug: Print raw output for inspection
        #print("Raw Kaggle API Output:")
        #print(result.stdout)  # Display the entire output for debugging

        # Parse the output into structured data
        leaderboard_data = []
        output_lines = result.stdout.strip().split("\n")

        # Skip the header line (assume the first line is the header)
        for line in output_lines[2:]:
            try:
                # Use re.split to handle multiple spaces
                fields = re.split(r'\s{2,}', line.strip())  # Split by 2 or more spaces

                # Debug: Print parsed fields
                #print("Parsed fields:", fields)

                # Update parsing logic to match the correct structure
                rank = int(fields[0])  # First column: rank
                team = fields[1]  # Second column: team name
                submission_date = fields[-2]  # Second-to-last column: submission date
                score = float(fields[-1])  # Last column: score

                # Append parsed data as a dictionary
                leaderboard_data.append({
                    "rank": rank,
                    "team": team,
                    "submission_date": submission_date,
                    "score": score
                })
            except (ValueError, IndexError) as e:
                # Log the error and skip invalid lines
                print(f"ValueError while parsing: {fields} -> {e}")
                continue

        # Update ranks to ensure they are sequential
        for i, entry in enumerate(leaderboard_data):
            entry["rank"] = i + 1

        return leaderboard_data

    except Exception as e:
        raise Exception(f"Failed to fetch leaderboard data: {str(e)}")
