"""
Base Agent Architecture for Multi-Agent Collaboration
Provides shared context, communication protocols, and collaboration capabilities
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from agents.llm_provider import get_llm_model
from langchain_core.prompts import PromptTemplate


class AgentMessage:
    """Represents a message passed between agents"""
    
    def __init__(self, sender: str, receiver: str, content: Any, message_type: str = "info"):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "message_type": self.message_type,
            "timestamp": self.timestamp.isoformat()
        }


class SharedContext:
    """Manages shared context and communication between agents"""
    
    def __init__(self):
        self.data = {}
        self.messages = []
        self.agent_registry = {}
        self.workflow_history = []
    
    def set(self, key: str, value: Any, agent_id: str = None):
        """Set a value in shared context"""
        self.data[key] = {
            "value": value,
            "set_by": agent_id,
            "timestamp": datetime.now()
        }
    
    def get(self, key: str, default=None):
        """Get a value from shared context"""
        if key in self.data:
            return self.data[key]["value"]
        return default
    
    def register_agent(self, agent_id: str, agent_instance):
        """Register an agent in the context"""
        self.agent_registry[agent_id] = agent_instance
    
    def send_message(self, message: AgentMessage):
        """Send a message between agents"""
        self.messages.append(message)
        
        # Deliver message to recipient if registered
        if message.receiver in self.agent_registry:
            recipient = self.agent_registry[message.receiver]
            recipient.receive_message(message)
    
    def get_messages_for(self, agent_id: str) -> List[AgentMessage]:
        """Get all messages for a specific agent"""
        return [msg for msg in self.messages if msg.receiver == agent_id]
    
    def log_workflow_step(self, step: str, agent_id: str, result: Any):
        """Log workflow steps for debugging and analysis"""
        self.workflow_history.append({
            "step": step,
            "agent_id": agent_id,
            "result": result,
            "timestamp": datetime.now()
        })


class BaseAgent(ABC):
    """Abstract base class for all educational agents"""
    
    def __init__(self, agent_id: str, specialization: str):
        self.agent_id = agent_id
        self.specialization = specialization
        self.shared_context: Optional[SharedContext] = None
        self.llm = get_llm_model()
        self.inbox = []
        self.collaboration_history = []
    
    def set_shared_context(self, context: SharedContext):
        """Set the shared context and register this agent"""
        self.shared_context = context
        self.shared_context.register_agent(self.agent_id, self)
    
    def send_message(self, receiver_id: str, content: Any, message_type: str = "info"):
        """Send a message to another agent"""
        if self.shared_context:
            message = AgentMessage(self.agent_id, receiver_id, content, message_type)
            self.shared_context.send_message(message)
            return message
        return None
    
    def receive_message(self, message: AgentMessage):
        """Receive a message from another agent"""
        self.inbox.append(message)
        self.process_message(message)
    
    def process_message(self, message: AgentMessage):
        """Process an incoming message - override in subclasses"""
        pass
    
    def collaborate_with(self, other_agent_id: str, task: str, data: Any) -> Any:
        """Collaborate with another agent on a specific task"""
        collaboration_request = {
            "task": task,
            "data": data,
            "requester": self.agent_id,
            "timestamp": datetime.now()
        }
        
        response = self.send_message(other_agent_id, collaboration_request, "collaboration_request")
        self.collaboration_history.append(collaboration_request)
        return response
    
    def get_context(self, key: str, default=None):
        """Get data from shared context"""
        if self.shared_context:
            return self.shared_context.get(key, default)
        return default
    
    def set_context(self, key: str, value: Any):
        """Set data in shared context"""
        if self.shared_context:
            self.shared_context.set(key, value, self.agent_id)
    
    def log_step(self, step: str, result: Any):
        """Log a workflow step"""
        if self.shared_context:
            self.shared_context.log_workflow_step(step, self.agent_id, result)
    
    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing method - must be implemented by subclasses"""
        pass
    
    def get_collaboration_context(self) -> Dict[str, Any]:
        """Get relevant context for collaboration"""
        return {
            "agent_id": self.agent_id,
            "specialization": self.specialization,
            "available_data": list(self.shared_context.data.keys()) if self.shared_context else [],
            "recent_messages": [msg.to_dict() for msg in self.inbox[-5:]],  # Last 5 messages
            "collaboration_history": self.collaboration_history[-3:]  # Last 3 collaborations
        }
    
    def create_collaborative_prompt(self, base_template: str, collaboration_data: Dict[str, Any]) -> PromptTemplate:
        """Create a prompt that includes collaboration context"""
        enhanced_template = f"""
{base_template}

COLLABORATION CONTEXT:
- Previous agent insights: {collaboration_data.get('previous_insights', 'None')}
- Shared analysis: {collaboration_data.get('shared_analysis', 'None')}
- Other agent feedback: {collaboration_data.get('agent_feedback', 'None')}

Please consider this collaborative context in your response and build upon the insights from other agents.
"""
        
        # Extract all variables from the enhanced template
        import re
        variables = re.findall(r'\{(\w+)\}', enhanced_template)
        
        return PromptTemplate(
            input_variables=list(set(variables)),
            template=enhanced_template
        )