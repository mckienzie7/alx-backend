#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(
        self, start_index: int = None, page_size: int = 10
    ) -> Dict:
        """
        Get hypermedia index with deletion resilience.

        Args:
            start_index (int): Start index of the current page.
            page_size (int): Size of items required in the current page.

        Returns:
            Dict[int, int|List[List]|None]: A dictionary with the following:
                * index
                * next_index
                * page_size
                * data
        """
        focus = []
        dataset = self.indexed_dataset()
        start_index = 0 if start_index is None else start_index
        keys = sorted(dataset.keys())
        assert 0 <= start_index <= keys[-1]
        [
            focus.append(i)
            for i in keys if i >= start_index and len(focus) <= page_size
        ]
        data = [dataset[v] for v in focus[:-1]]
        next_index = focus[-1] if len(focus) - page_size == 1 else None
        return {
            'index': start_index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index
        }


if __name__ == "__main__":
    server = Server()

    try:
        server.get_hyper_index(300000, 100)
    except AssertionError:
        print("AssertionError raised when out of range")

    start_index = 3
    page_size = 2

    print(
        "Number of items in indexed dataset: {}".format(
            len(server.indexed_dataset())
        )
    )

    res = server.get_hyper_index(start_index, page_size)
    print(res)

    print(server.get_hyper_index(res.get('next_index'), page_size))

    del server.indexed_dataset()[res.get('index')]
    print(
        "Number of items in indexed dataset after deletion: {}".format(
            len(server.indexed_dataset())
        )
    )

    print(server.get_hyper_index(start_index, page_size))
    print(server.get_hyper_index(res.get('next_index'), page_size))
