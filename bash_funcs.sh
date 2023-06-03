#!/bin/bash

# Define remote server information
REMOTE_SERVER="user@remote-server"


# Function to append a string to bash_funcs.sh
append_to_file() {
  local comment="$1"
  local function="$2"
  
  # Add comment if provided
  if [ -n "$comment" ]; then
    printf "\n%s" "# $comment" >> /home/serialdev/Desktop/workdir/personal/sdev-machine/bash_funcs.sh
    printf "\n%s" "# $comment" >> /home/serialdev/bin/bash_funcs.sh


  fi
  
  # Append the function
  printf "\n%s" "$function" >> /home/serialdev/Desktop/workdir/personal/sdev-machine/bash_funcs.sh

  printf "\n%s" "$function" >> /home/serialdev/bin/bash_funcs.sh

  echo "Function appended to bash_funcs.sh"
}

# Call the function with the provided command-line argument
# append_to_file "$1"


# Make my_functions.sh executable
#chmod +x bash_funcs.sh

# Move my_functions.sh to a directory in the PATH
#sudo cp bash_funcs.sh /home/serialdev/bin/bash_funcs && source /home/serialdev/bin/bash_funcs


# Create symlink
#sudo ln -s "$(pwd)/bash_funcs.sh" /home/serialdev/bin/bash_funcs

# Source it
# source /home/serialdev/bin/bash_funcs



# JSON Pretty Print with jq

json_pp() {
  jq . "$1"
}

# Extract Values from JSON Array

extract_values() {
  jq -r ".[] | .key" "$1"
}

# Filter JSON Objects by Key

filter_by_key() {
  jq "map(select(.key == \"value\"))" "$1"
}

# Count JSON Objects

count_objects() {
  jq length "$1"
}

# Sort JSON Array

sort_array() {
  jq "sort_by(.key)" "$1"
}

# Sum JSON Number Values

sum_numbers() {
  jq "[.[] | .key] | add" "$1"
}

# Filter JSON Objects by Condition

filter_by_condition() {
  jq "map(select(.key > 10))" "$1"
}

# Merge JSON Files

merge_json_files() {
  jq -s "reduce .[] as \$item ({}; . * \$item)" "$@"
}

# Extract JSON Key-Value Pairs

extract_key_value_pairs() {
  jq -r "to_entries[] | \"\(.key), \(.value)\"" "$1"
}

# Extract Unique Values from JSON Array

extract_unique_values() {
  jq -r ".[] | .key" "$1" | sort -u
}

# Generate Dummy JSON data using jq

generate_dummy_json() {
  jq -n '{
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com",
    "address": {
      "street": "123 Main Street",
      "city": "New York",
      "country": "USA"
    },
    "skills": ["Python", "JavaScript", "SQL"]
  }' 
}

# Create a Directory and Navigate to it

mkcd() {
  mkdir -p "$1" && cd "$1"
}

# Remove a Directory and its Contents Recursively

rmd() {
  rm -rf "$1"
}

# Generate SSH Key Pair

generate_ssh_key() {
  ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
  echo "SSH key pair generated"
}


# Copy Local File to Remote Server via SSH

scp_file() {
  local file="$1"
  local destination="$2"
  scp "$file" "$REMOTE_SERVER":"$destination"
  echo "File copied to remote server"
}

# SSH into Remote Server

# SSH into Remote Server
ssh_connect() {
  ssh "$REMOTE_SERVER"
}

# Format Python Code with Black

format_python_code() {
  black "$1"
}

# Analyze Python Code with Bandit

analyze_python_code() {
  bandit -r "$1"
}

# Create a New Screen Session

create_screen_session() {
  screen -S "$1"
}

# List Active Screen Sessions

list_screen_sessions() {
  screen -ls
}

# Attach to an Existing Screen Session

attach_to_screen_session() {
  screen -r "$1"
}

# Detach from a Screen Session

detach_screen_session() {
  screen -d "$1"
}

# Send Command to a Running Screen Session

send_command_to_screen_session() {
  screen -S "$1" -X stuff "$2\n"
}

# Enable Scrollback Buffer in Screen

enable_screen_scrollback() {
  screen -S "$1" -X eval "scrollback 10000"
}

# Take Screenshot of a Screen Session

screenshot_screen_session() {
  screen -S "$1" -X hardcopy "$2"
  echo "Screenshot saved"
}

# Lock a Screen Session

lock_screen_session() {
  screen -S "$1" -X lockscreen on
  echo "Screen session locked"
}

# Kill a Screen Session

kill_screen_session() {
  screen -S "$1" -X quit
  echo "Screen session killed"
}

# Show Git Branch Tree

git_branch_tree() {
  git log --graph --abbrev-commit --decorate --format=format:"%C(auto)%h %d %s %C(black)%C(bold)%cr" --all
}

# Display Git Commit History

git_commit_history() {
  git log --pretty=format:"%C(auto)%h %C(bold)%<(20,trunc)%an %C(dim white)%<(25,trunc)%cd %C(auto)%s"
}

# List Remote Git Branches

git_list_remote_branches() {
  git branch -r
}

# Merge a Git Branch into Current Branch

git_merge_branch() {
  git merge "$1"
}

# Rebase Current Branch onto Another Branch

git_rebase_branch() {
  git rebase "$1"
}

# Amend the Last Git Commit

git_amend_commit() {
  git commit --amend --no-edit
}

# Create and Switch to a Git Tag

git_create_tag() {
  git tag "$1" && git checkout "$1"
}

# Show Git Tag Details

git_show_tag() {
  git show "$1"
}

# Cherry-pick a Git Commit

git_cherry_pick() {
  git cherry-pick "$1"
}

# Remove Untracked Files and Directories

git_clean() {
  git clean -df
}


