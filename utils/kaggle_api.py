import re
import subprocess

def fetch_leaderboard_data(competition_name, max_rows=100):
    """
    Fetch and parse leaderboard data from Kaggle API, limiting to a maximum of max_rows.
    The returned list will have sequentially assigned ranks for the subset.
    """
    try:
        # Run the Kaggle API command
        result = subprocess.run(
            ["kaggle", "competitions", "leaderboard", "-c", competition_name, "--show"],
            capture_output=True,
            text=True,
            check=True  # This will raise CalledProcessError if returncode is non-zero
        )

        # Parse the output into structured data
        parsed_leaderboard = []
        output_lines = result.stdout.strip().split("\n")

        # Skip the header and separator lines (typically first two lines of Kaggle CLI output)
        for line in output_lines[2:]:
            try:
                fields = re.split(r'\s{2,}', line.strip())

                if len(fields) < 4: # Basic check for Rank, Team, Date, Score
                    # print(f"Skipping malformed line (not enough fields): {line.strip()}")
                    continue

                rank_str = fields[0]
                score_str = fields[-1]
                submission_date_str = fields[-2]

                # Determine team name parts: everything between rank and submission_date
                if len(fields) == 4: # Rank, Team, Date, Score
                    team_name_parts = [fields[1]]
                else: # Rank, Team Part 1, Team Part 2, ..., Date, Score
                    team_name_parts = fields[1:-2]
                
                team = " ".join(team_name_parts).strip()

                # Attempt to convert rank and score, skip line on error
                try:
                    # rank_from_api = int(rank_str) # Original rank from API, if needed
                    score = float(score_str)
                except ValueError:
                    # print(f"Skipping line due to conversion error for rank/score: {line.strip()}")
                    continue
                
                # We don't strictly need rank_from_api if we re-rank the subset anyway.
                # Score and team are the most crucial for sorting and display.
                parsed_leaderboard.append({
                    # "original_rank": rank_from_api,
                    "team": team,
                    "submission_date": submission_date_str,
                    "score": score
                })

            except (IndexError) as e: # Catch specific errors if fields are missing
                # print(f"Error parsing line due to missing fields: '{line.strip()}' -> {e}. Fields: {fields}")
                continue
            except Exception as e: # Catch any other unexpected parsing error for a line
                # print(f"Generic error parsing line: '{line.strip()}' -> {e}. Fields: {fields}")
                continue
        
        # --- Limit to max_rows ---
        # The Kaggle CLI --show typically already sorts by score.
        # Taking the first max_rows entries from the parsed list should give the top entries.
        if not parsed_leaderboard:
            return []
            
        # Sort by score (descending) to ensure correct order before limiting and re-ranking.
        # Kaggle CLI output for --show is usually sorted, but this is a safeguard.
        # Adjust `reverse=False` if lower scores are better for the competition.
        parsed_leaderboard.sort(key=lambda x: x['score'], reverse=True) 

        limited_leaderboard_subset = parsed_leaderboard[:max_rows]

        # --- Re-rank the limited subset sequentially (1, 2, 2, 4 style) ---
        final_ranked_leaderboard = []
        if not limited_leaderboard_subset:
            return []

        current_rank = 0
        last_score = -float('inf') # Initialize to a very small number (for higher-is-better scores)
                                  # Or float('inf') if lower scores are better
        
        for i, entry in enumerate(limited_leaderboard_subset):
            # Standard competition ranking (dense ranking: 1, 2, 2, 4)
            if entry['score'] != last_score: 
                current_rank = i + 1 
            last_score = entry['score']
            
            final_ranked_leaderboard.append({
                "rank": current_rank,
                "team": entry["team"],
                "submission_date": entry["submission_date"],
                "score": entry["score"]
            })

        return final_ranked_leaderboard

    except subprocess.CalledProcessError as e:
        # Handle errors from the subprocess run, e.g., competition not found
        # print(f"Kaggle API command failed for '{competition_name}'. Error: {e.stderr}")
        raise Exception(f"Failed to fetch leaderboard data from Kaggle API for '{competition_name}': {e.stderr}")
    except Exception as e:
        # Handle other potential errors
        # print(f"An unexpected error occurred while fetching leaderboard for '{competition_name}': {str(e)}")
        raise Exception(f"Failed to fetch leaderboard data for '{competition_name}': {str(e)}")