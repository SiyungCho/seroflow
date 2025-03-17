"""
Module: chunker

This module provides functionality for partitioning or chunking ETL execution. 
It defines several chunker classes that facilitate the division of large datasets
or processing tasks into smaller, more manageable segments during execution.
Any custom chunker created should derive from the Chunker class.

Key Components:
    - Chunker: Base class that outlines the common interface and behavior for all chunking strategies.
    - DirectChunker: Implements a straightforward approach to splitting tasks directly into discrete chunks.
    - RecursiveChunker: Employs a recursive strategy to further subdivide tasks into smaller chunks, useful for complex or nested data processing scenarios.
"""

from .chunker import Chunker
from .direct_chunker import DirectChunker
from .recursive_chunker import RecursiveChunker
