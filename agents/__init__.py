"""
MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant
Agent Module Package
"""

from .diagnostic import DiagnosticAgent
from .reasoning import ReasoningAgent
from .treatment import TreatmentAgent
from .followup import FollowUpAgent

__all__ = [
    'DiagnosticAgent',
    'ReasoningAgent', 
    'TreatmentAgent',
    'FollowUpAgent'
]
