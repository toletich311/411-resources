import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    def __init__(self):

        """Initializes an empty ring with no boxers as a list.
        
        Attributes: 

            ring (list[Boxer]): A list that is currently storing all the boxers within
            the ring. 
         
        """

        self.ring: List[Boxer] = []
        logger.info("Ring has been initialized with an empty ring.")

    def fight(self) -> str:

        """Simulates a fight between the boxers. Starts by checking whether there are
        at least two boxers within the ring. If there are less than we throw an error. 
        Then we take two boxers and calculate their fighting skills and compare the difference
        and update the stats. 

        Args: 
            an instance of the ringModel class.

        Returns: 
            winner.name: the str name of the winning boxer.

        Raises:
        ValueError: If there are less than two boxers in the ring.

        """

        logger.info("Starting a fight in the ring.")
        if len(self.ring) < 2:
            logger.warning("There are not enough boxers.")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()
        logger.info(f"Initializing fight between Boxer 1: {boxer_1.name} vs. Boxer 2: {boxer_2.name}")

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)
        logger.info(f"{boxer_1.name} fighting skills: {skill_1}")
        logger.info(f"{boxer_2.name} fighting skills: {skill_2}")
                    


        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))
        logger.info(f"Pure skill difference: {delta}")
        logger.info(f"Normalized skill difference: {normalized_delta}")

        random_number = get_random()

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        logger.info(f"{winner.name} has won the fight.")
        logger.info(f"{loser.name} has lost the fight.")
        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')

        self.clear_ring()
        logger.info("Ring has been cleared for next fight.")

        return winner.name

    def clear_ring(self):

        """Clears the ring by removing all the boxers from the ring. 
        Empties the current list of boxers. 
        
        returns: 
            Nothing. But modifies the list of boxers by emptying it. 
        
        """

        if not self.ring:
            logger.info("Ring is already empty.")
            return
        logger.info("Clearing the ring.")
        self.ring.clear()
        logger.info("Ring has been cleared.")

    def enter_ring(self, boxer: Boxer):

        """Adds a boxer to the ring if it is an instance of the Boxer class 
        and if there is room within the ring for another Boxer. Throws errors
        if the ring is full or if the boxer is not an instance of the Boxer class.

        Args:
           A boxer instance
        
        Returns:
            Nothing. But modifies the list of boxers by adding a boxer to it.
        
        Raises:
            TypeError: If the input is not a Boxer instance.
            ValueError: If there are already two boxers in the ring. 
        """
        
        logger.info(f"{boxer.name} is trying to enter into the ring")
        if not isinstance(boxer, Boxer):
            logger.warning("Invalid type: Expected 'Boxer'")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        if len(self.ring) >= 2:
            logger.warning("The ring is full, cannot add anymore boxers.")
            raise ValueError("Ring is full, cannot add more boxers.")

        self.ring.append(boxer)
        logger.info(f"Boxer {boxer.name} has entered the ring.")

    def get_boxers(self) -> List[Boxer]:

        """ returns the current list of boxers. 

        Returns:
            The current list of Boxers within the ring. 
        
        """

        if not self.ring:
            pass
        else:
            pass
        logger.info("These are the current boxers in the ring: {[boxer.name for boxer in self.ring]} ")
        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        """Arbrituarily calculates the fighting skill of each boxer based 
        on a custon formula using the boxers weight, name, length, reach, and age.

        Args:
            an instance of the Boxer class 

        Returns:
            a float value representing the skill level of the boxer. 
        """
        
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        logger.info(f"{boxer.name} has a fighting skill of {skill}")
        return skill
