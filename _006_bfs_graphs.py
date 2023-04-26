from collections import deque, defaultdict
from typing import NamedTuple, Optional
from pprint import pp


class Person(NamedTuple):
    name: str
    is_mango_seller: bool = False


PersonGraph = defaultdict[Person, list[Person]]


def find_closest_mango_seller(people: PersonGraph, person: Person) -> Optional[Person]:
    """Dict-based approach of breadth-first search as described in the book.
    Graph nodes are represented as dict keys.
    Related nodes are values of dict."""
    search_queue: deque[Person] = deque(people[person])
    checked_people: set[Person] = set()
    while search_queue:
        person = search_queue.popleft()
        if person in checked_people:
            continue
        if person.is_mango_seller:
            return person
        search_queue += people[person]
        checked_people.add(person)


def main() -> None:
    me = Person('Danila')
    developer = Person('Dev')
    manager = Person('Manager')
    designer = Person('Designer')
    artist = Person('ЯхудожникЯтаквижу')
    banana_seller = Person('Bananster')
    meat_seller = Person('Butcher')
    mango_seller1 = Person('Mango Boy 1', True)
    mango_seller2 = Person('Mango Man 2', True)
    mango_seller3 = Person('Mango Mega Man 3', True)

    people: PersonGraph = defaultdict(list, {
        me: [developer, banana_seller],
        developer: [manager, designer],
        designer: [me, artist],
        artist: [mango_seller1],
        banana_seller: [mango_seller2, meat_seller],
        meat_seller: [mango_seller3, me],
    })

    mango_seller = find_closest_mango_seller(people, me)
    print(mango_seller.name if mango_seller else None)


class Person2(NamedTuple):
    name: str
    friends: list["Person2"]
    is_mango_seller: bool = False

    @classmethod
    def create(cls, name: str, friends: Optional[list["Person2"]] = None, is_mango_seller: bool = False):
        return cls(name, friends if friends else [], is_mango_seller)

    def __hash__(self):
        return hash((self.name, self.is_mango_seller))


def is_person_a_mango_seller2(person: Person2) -> bool:
    return person.is_mango_seller


def is_last_char_of_name_a_digit2(person: Person2) -> bool:
    return person.name[-1].isdigit()

def is_first_char_of_name_a_digit2(person: Person2) -> bool:
    return person.name[0].isdigit()


def find_closest_mango_seller2(person: Person2, *, key=is_person_a_mango_seller2) -> Optional[Person2]:
    """Another approach where each node stores related nodes as list in its `friends` attribute."""
    search_queue: deque[Person2] = deque(person.friends)
    checked_people: set[Person2] = set()
    while search_queue:
        person = search_queue.popleft()
        if person in checked_people:
            continue
        if key(person):
            return person
        search_queue += person.friends
        checked_people.add(person)


def main2() -> None:
    me = Person2.create('Danila')
    developer = Person2.create('Dev')
    manager = Person2.create('Manager')
    designer = Person2.create('Designer')
    artist = Person2.create('ЯхудожникЯтаквижу')
    banana_seller = Person2.create('Bananster')
    meat_seller = Person2.create('Butcher')
    mango_seller1 = Person2.create('Mango Boy 1', [], True)
    mango_seller2 = Person2.create('Mango Man 2_', [], True)
    mango_seller3 = Person2.create('Mango Mega Man 3_', [], True)

    me.friends.extend([developer, banana_seller])
    developer.friends.extend([manager, designer])
    designer.friends.extend([me, artist])
    artist.friends.extend([mango_seller1])
    banana_seller.friends.extend([mango_seller2, meat_seller])
    meat_seller.friends.extend([mango_seller3, me])

    mango_seller = find_closest_mango_seller2(me)
    print(mango_seller and mango_seller.name)
    mango_seller = find_closest_mango_seller2(me, key=is_last_char_of_name_a_digit2)
    print(mango_seller and mango_seller.name)
    mango_seller = find_closest_mango_seller2(me, key=is_first_char_of_name_a_digit2)
    print(mango_seller and mango_seller.name)


if __name__ == '__main__':
    main()
    main2()
