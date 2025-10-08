import sys
import os
import re

def parse_worklog(source_file_path, repo_name, dest_dir):
    """
    Parses a WORKLOG.md file, splitting it into multiple files, one for each date entry.
    Each new file contains the original header and the content for a single date.
    """
    try:
        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Source file not found at {source_file_path}")
        return

    # Find the first date heading (###) to separate the header from the log entries
    first_heading_match = re.search(r'^###\s+', content, re.MULTILINE)
    if not first_heading_match:
        print("No date entries (###) found in the worklog. Nothing to parse.")
        return

    header_content = content[:first_heading_match.start()]
    log_content = content[first_heading_match.start():]

    # Split the log content by date headings. The regex keeps the headings.
    # It splits on any line that starts with '### '
    date_entries = re.split(r'(^###\s+.*$)', log_content, flags=re.MULTILINE)

    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    # The split results in ['', '### date1', 'content1', '### date2', 'content2', ...]
    # So we process the list in pairs (heading, content)
    for i in range(1, len(date_entries), 2):
        heading = date_entries[i].strip()
        entry_content = date_entries[i+1].strip()

        # Extract the date from the heading, removing '###'
        date_str = heading.replace('###', '').strip()
        
        # Sanitize the date for the filename (e.g., '07/10/25' -> '25-10-07')
        # This format (YY-MM-DD) sorts better chronologically
        parts = date_str.split('/')
        if len(parts) == 3:
            sanitized_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        else:
            # Fallback for unexpected date formats
            sanitized_date = re.sub(r'[^0-9a-zA-Z-]', '-', date_str)

        # Create the new filename and full path
        new_filename = f"{repo_name}-WORKLOG-{sanitized_date}.md"
        new_filepath = os.path.join(dest_dir, new_filename)

        # Combine the header with the single date entry
        final_content = f"{header_content.strip()}\n\n{heading}\n\n{entry_content}\n"

        # Write the new file
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✅ Created worklog file: {new_filepath}")


if __name__ == "__main__":
    # Expects 3 command-line arguments:
    # 1. Path to the source WORKLOG.md
    # 2. Repository name (for filename)
    # 3. Destination directory
    source_file = sys.argv[1]
    repo_name = sys.argv[2]
    destination_dir = sys.argv[3]
    parse_worklog(source_file, repo_name, destination_dir)
