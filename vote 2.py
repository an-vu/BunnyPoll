import os
import csv

class Poll:
    def __init__(self, name, vote_limit, description='', candidates=None):
        """
        Initializes a new Poll object with a name, vote limit, optional description, and candidates.

        Args:
            name (str): The name of the poll.
            vote_limit (int): The maximum number of votes allowed for this poll.
            description (str, optional): A description of the poll. Defaults to an empty string.
            candidates (Dict[str, int], optional): A dictionary of candidates with their respective vote counts. Defaults to None.
        """
        self.name = name
        self.description = description
        self.vote_limit = vote_limit
        self.candidates = candidates or {}
        self.total_votes = 0
        self.poll_closed = False

    def to_csv_row(self):
        """
        Converts the poll data to a format suitable for CSV file storage.

        Returns:
            List[str]: A list of strings representing the poll data, including name, description, 
                       and each candidate's vote count.
        """
        row = [self.name, self.description if self.description else '']
        for choice, votes in self.candidates.items():
            row.extend([choice, str(votes)])
        return row

    def cast_vote(self, candidate_name):
        """
        Casts a vote for a specified candidate if the poll is open and the candidate exists.

        Args:
            candidate_name (str): The name of the candidate for whom the vote is cast.

        Returns:
            bool: True if the vote was successfully cast, False otherwise.
        """
        if self.poll_closed or candidate_name not in self.candidates:
            return False
        self.candidates[candidate_name] += 1
        self.total_votes += 1
        self.poll_closed = self.total_votes >= self.vote_limit
        return True

    def __str__(self): # Debugging
        return f"Poll(name={self.name}, description={self.description}, vote_limit={self.vote_limit}, candidates={self.candidates}, total_votes={self.total_votes}, poll_closed={self.poll_closed})"

class VotingSystem:
    def __init__(self, csv_file_path='polls.csv'):
        self.polls = {}
        self.poll_number = 1  # Initialize poll numbering
        current_dir = os.path.dirname(__file__)
        self.csv_file_path = os.path.join(current_dir, 'polls.csv')
        self.load_polls_from_csv()

    def create_poll(self, poll_name, description, choices, vote_limit=100):
        """
        Creates a new poll and saves it to the CSV file.

        Args:
            poll_name (str): Name of the poll.
            description (str): Description of the poll.
            choices (List[str]): List of choices for the poll.
            vote_limit (int, optional): The limit of votes allowed for the poll. Defaults to 100.
        """
        numbered_poll_name = f"poll{self.poll_number}: {poll_name}"
        self.poll_number += 1  # Increment for the next poll

        if numbered_poll_name not in self.polls and choices:
            choices_dict = {choice: 0 for choice in choices if choice}  # Exclude empty choices
            self.polls[numbered_poll_name] = Poll(poll_name, vote_limit, description, choices_dict)
            self.save_polls_to_csv()

    def load_polls_from_csv(self):
        """
        Loads poll data from the CSV file and initializes polls in the system.
        """
        try:
            with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Extract the poll number and name
                    poll_number_and_name, description, *choices_votes = row

                    # Check if the string contains a colon and split accordingly
                    if ":" in poll_number_and_name:
                        poll_name = poll_number_and_name.split(": ")[1]
                    else:
                        poll_name = poll_number_and_name

                    # Process choices and votes
                    choices_dict = {}
                    for i in range(0, len(choices_votes), 2):
                        choice = choices_votes[i]
                        votes = int(choices_votes[i + 1])
                        choices_dict[choice] = votes

                    self.polls[poll_number_and_name] = Poll(poll_name, 100, description, choices_dict)
        except FileNotFoundError:
            pass

    def get_poll_data(self, poll_name):
        """
        Retrieves the data of a specific poll.

        Args:
            poll_name (str): The name of the poll.

        Returns:
            dict: A dictionary containing the poll's data.
        """
        return self.polls.get(poll_name, Poll(None, None)).__dict__

    def save_polls_to_csv(self):
        """
        Saves current polls to the CSV file.
        """
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for poll in self.polls.values():
                writer.writerow(poll.to_csv_row())

    def delete_poll(self, poll_name):
        """
        Deletes a poll from the system and updates the CSV file.

        Args:
            poll_name (str): The name of the poll to delete.

        Returns:
            bool: True if the poll was successfully deleted, False otherwise.
        """
        if poll_name in self.polls:
            del self.polls[poll_name]
            self.save_polls_to_csv()
            return True
        return False

    def list_polls(self):
        """
        Lists the names of all polls currently in the system.

        Returns:
            List[str]: A list of poll names.
        """
        return list(self.polls.keys())
    
    def reload_polls_from_csv(self):
        """
        Clears the current polls and reloads them from the CSV file.
        """
        self.polls.clear()
        self.load_polls_from_csv()

    def modify_poll(self, old_name, new_name, description, choices):
        """
        Modifies an existing poll with new details.

        Args:
            old_name (str): The current name of the poll.
            new_name (str): The new name of the poll.
            description (str): The new description of the poll.
            choices (List[str]): The updated list of choices for the poll.
        """
        if old_name in self.polls:
            poll = self.polls.pop(old_name)
            poll.name = new_name
            poll.description = description
            poll.candidates = {choice: poll.candidates.get(choice, 0) for choice in choices}
            self.polls[new_name] = poll

    def export_poll_to_txt(self, poll_name):
        """
        Exports a specific poll's data to a text file.

        Args:
            poll_name (str): The name of the poll to export.

        Returns:
            bool: True if the poll was successfully exported, False otherwise.
        """
        poll = self.polls.get(poll_name)
        if poll:
            file_path = os.path.join(os.path.dirname(self.csv_file_path), f"{poll_name}.txt")
            content = f"Name: {poll.name}\nDescription: {poll.description}\n\n"
            content += "\n".join([f"{choice} - {votes}" for choice, votes in poll.candidates.items()])
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        return False

    def cast_vote(self, poll_name, candidate_name):
        return self.polls.get(poll_name, Poll(None, None)).cast_vote(candidate_name)