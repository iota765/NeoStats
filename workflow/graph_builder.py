from langgraph.graph import StateGraph, START, END
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from nodes.web_query import rewrite_query, web_search_node
from nodes.direct_generation import generate_direct
from nodes.relevance import is_relevant
from routes.route import (
    route_after_context,
    route_after_decide,
    route_after_direct,
    route_after_relevance,
)
from nodes.retrieve_decision import decide_retrieval
from nodes.generate_from_context import generate_from_context
from nodes.retrieve import retrieve
from config.state import State


#nodes
g=StateGraph(State)
g.add_node("decide_retrieval", decide_retrieval)
g.add_node("generate_direct", generate_direct)
g.add_node("retrieve", retrieve)

g.add_node("is_relevant",is_relevant)
g.add_node("generate_from_context", generate_from_context)
g.add_node("rewrite_query", rewrite_query)
g.add_node("web_search_node", web_search_node)

#edges
g.add_edge(START, "decide_retrieval")
g.add_conditional_edges(
    "decide_retrieval",
    route_after_decide,
    {
        "generate_direct": "generate_direct",
        "retrieve": "retrieve",
    },
)
g.add_conditional_edges(
    "generate_direct",
    route_after_direct,
    {
        "rewrite_query": "rewrite_query",
        "end": END,
    },
)
g.add_edge("retrieve", "is_relevant")

g.add_conditional_edges(
    "is_relevant",
    route_after_relevance,
    {
        "generate_from_context": "generate_from_context",
        "rewrite_query": "rewrite_query",
    },
)

g.add_edge("rewrite_query","web_search_node")
g.add_edge("web_search_node","is_relevant")
g.add_conditional_edges(
    "generate_from_context",
    route_after_context,
    {
        "rewrite_query": "rewrite_query",
        "end": END,
    },
)

app = g.compile()
