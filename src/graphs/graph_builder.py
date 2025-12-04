from langgraph.graph import StateGraph, START, END
from src.llms.groq_llm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    
    def build_topic_graph(self):
        """
            Build a graph to generate blogs based on a topic
        """
        self.blog_node_obj = BlogNode(self.llm)
        # Add Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)

        # Add Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        compiled_graph = self.graph.compile()

        return compiled_graph
    

    def setup_graph(self, usecase: str):
        """Function that runs builds graph based on a specific usecase

        Args:
            usecase (str): Usecase
        """
        if usecase == "topic":
            compiled_graph = self.build_topic_graph()

            return compiled_graph
        
    
# Below code is for the langsmith -> langgraph studio
llm = GroqLLM().get_llm()

# Get the graph
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_topic_graph()