'''
    SCHOOL ELECTION.

    Creation of a program which purpose is to control the vote for various
    proposal in a school.

    The student have to insert:
                                - Name
                                - Surname
                                - ID

    When the fields are inserted the studen can choose between this action:
                                - Create a new proposal.
                                - Vote for an existing proposal.
                                - View the proposal, who created it and the
                                  number of votes. A proposal can be created
                                  by two student.
                                - Terminate the program.

    A student can insert an unlimeted quantity of proposal.
    A student can vote for every proposal, but only one time for every proposal.

    The python client have to use a REDIS server for managing the data from
    the election.

    Data structure used:
                                - ZSET for insert the election results.
                                  In this way every proposal have a number
                                  related and is possibile to automatically
                                  order the proposal.
                                - HSET for the proposal and the information.
                                  The hset will contain.
                                                - Number of the proposal.
                                                - Description of the proposal.
                                                - Creators.
                                                - Numbers of vote.


    #########################################################################
    ATTENTION.
    What we have to control:
    - It's impossibile to insert two identical proposal. If a student insert
      an existing proposal the program have to react consequetially.
    - The initial vote of every proposal have to be set on 0.

'''

import redis
import sys


class Proposals:
    '''
        Redis initialization.
    '''

    def __init__(self):
        self.redis = redis.Redis(host             = 'localhost',
                                 port             = 6379,
                                 db               = 0,
                                 charset          = 'utf-8',
                                 decode_responses = True)

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def home(self):
        '''

            _______
           !      !
           ! HOME !
           !______!


            -----------------------------------------------------------------
            Student log and show the possible action to the users.
            -----------------------------------------------------------------
        '''

        print('Insert your data to vote and visualize the proposal.\n')
        print('\n')
        while True:
            while True:
                try:
                    print("-" * 90)
                    self.alumn_name    = str(input('Insert you name:\t').title())
                    self.alumn_surname = str(input('Insert your surname:\t').title())
                    self.alumn_ID      = int(input('Insert your students ID:\t'))
                    print("-" * 90)
                    self.insert_student(self.alumn_name, self.alumn_surname)
                    break
                except ValueError:
                    print('Insert a numeric ID')
                except TypeError as e:
                    print(e)

            while True:
                try:
                    print('What do you wanto to do?\n\n\n'
                          'n = New proposal\n'
                          'v = Vote a proposal\n'
                          'd = Proposal description\n'
                          'e = Exit')
                    scelta = str(input())

                    n_option = ['n', 'N']
                    v_option = ['v', 'V']
                    d_option = ['d', 'D']
                    e_option = ['e', 'E']
                    if scelta in n_option or \
                            scelta in v_option or \
                            scelta in d_option or \
                            scelta in e_option:
                        pass
                    else:
                        raise ValueError('You have not entered any of the possible choices')
                except ValueError as err:
                    print(err)

                if scelta in n_option:
                    prop = input('Insert your proposal\n')
                    self.insert_proposal(prop)
                elif scelta in v_option:
                    print('Vote one proposal\n')
                    self.proposal_vote()
                elif scelta in d_option:
                    if [key for key in self.redis.scan_iter('proposal:*')]:
                        self.read_proposal()
                    else:
                        print('There are no proposal yet\n')
                elif scelta in e_option:
                    sys.exit("Thanks! See you soon!")
                else:
                    print('\n There are no proposal yet')

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def read_proposal(self):
        '''

            _______________________
           !                       !
           ! READ PROPOSAL SECTION !
           !_______________________!


        ----------------------------------------------------------------------
            Read the keys in Redis wich correspond to 'proposal:*'
            The student see on the screen all the proposal with:
                 - The creator
                 - Number of vote
                 - Description.

        ---------------------------------------------------------------------

        '''
        print('')
        for key in self.redis.scan_iter('proposal:*'):
            proposer = self.redis.hget(key, "proposer")
            desc = self.redis.hget(key, 'desc')
            votes = self.redis.hget(key, 'votes')
            print(f'{key.title()}\t\tProposed by: {proposer}\n'
                  f'Description: {desc}\t\t{votes} votes\n'
                  f'{"-" * 95}')


    # ========================================================================
    # ========================================================================
    # ========================================================================

    def insert_student(self, name, surname):
        '''
        Parameters
        ----------
        name : str
            Name of the student.
        surname : str
            Surname of the student.

        ---------------------------------------------------------------------

        The funciton insert name and surname in a Redis set.
        The key of the set is student:student_ID

        ----------------------------------------------------------------------

        '''
        if f'student:{self.alumn_ID}' in self.redis.scan_iter('student:*'):
            if self.redis.get(f'student:{self.alumn_ID}') == f'{name} {surname}':
                pass
            else:
                raise TypeError('Insert valid credentials')
        self.redis.set(f'student:{str(self.alumn_ID)}', f'{name} {surname}')

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def insert_proposal(self, sugg):
        '''

            _________________________
           !                         !
           ! INSERT PROPOSAL SECTION !
           !_________________________!


        ---------------------------------------------------------------------
        Parameters
        ----------
        sugg : str
            The propose insert in the home function.

        ---------------------------------------------------------------------

        The function initialize the proposal of the student. It's inserted in
        Redis in a hset with key "proposal:n_proposal"
                The hset contain:
                            - desc -> description of the proposal.
                            - proposer -> who have create the proposal?
                            - votes -> numbers of vote of the proposal.
        ---------------------------------------------------------------------

        '''
        proposte = [key for key in self.redis.scan_iter('proposal:*')]
        proposte.sort()

        if sugg in [self.redis.hget(key, 'desc') for key in proposte]:
            print('La proposal esiste già')
        elif len(proposte) == 0:

            self.redis.hset('proposal:1', 'desc', f'{sugg}')
            self.redis.hset('proposal:1', 'proposer',
                            str(self.redis.get(f'student:{str(self.alumn_ID)}')))
            self.redis.hset('proposal:1', 'votes', 0)
            self.redis.lpush('proposer:proposal:1', str(self.alumn_ID))
            self.redis.zadd('votes:proposal', {'proposal:1': 0})
            print('Proposal correctly inserted')
            # created redis list with proposal:1 ID
        else:
            last_proposal = int(proposte[-1][proposte[-1].find(':') + 1:])
            self.redis.hset(f"proposal:{last_proposal + 1}", 'desc', f'{sugg}')
            self.redis.hset(f"proposal:{last_proposal + 1}", 'proposer',
                            str(self.redis.get(f'student:{self.alumn_ID}')))
            self.redis.hset(f"proposal:{last_proposal + 1}", 'votes', 0)
            # created list with proposal:last_proposal+1  ID
            self.redis.zadd('votes:proposal', {f'proposal:{last_proposal + 1}': 0})
            print('Proposal correctly inserted')

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def proposal_vote(self):
        '''

            _______________
           !              !
           ! VOTE SECTION !
           !______________!


            -----------------------------------------------------------------
            In this section is possible to vote for a proposal.
            Insert the nuber correspondant to a proposal ex. proposal:5, I
            need to insert 5.
            Every student can vote one time for one proposal but he can vote
            for every proposal.
            -----------------------------------------------------------------
        '''

        proposal = [key for key in self.redis.scan_iter('proposal:*')]
        proposal.sort()

        if len(proposal) == 0:
            print("There are no vote yet! Visit the section" \
                  "new proposal to be the first")
        else:
            print('Vote one of the following proposal:')
            self.read_proposal()
            proposal_list = [int(key[key.find(':') + 1:]) for key in
                              self.redis.scan_iter('proposal:*')]
            while True:
                try:
                    choice = int(input('Write the name of the propoal you want to vote\n'))
                    if choice in proposal_list:
                        elector_list = self.redis.lrange(f'elector:proposal:{choice}', 0, -1)
                        if str(self.alumn_ID) not in elector_list:
                            self.redis.lpush(f'elector:proposal:{choice}',
                                             self.alumn_ID)
                            self.redis.hincrby(f'proposal:{choice}', 'votes', 1)
                            self.redis.zincrby('votes:proposal', 1, f'proposal:{choice}')
                            print('\nThanks for your vote\n')
                        else:
                            print("You already voted for this proposal, choose another one")
                            break
                    else:
                        raise ValueError('Insert the number of an existent proposal')
                    break
                except ValueError:
                    print('Insert an integer number')


if __name__ == '__main__':
    a = Proposals()
    a.home()
