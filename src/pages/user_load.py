import streamlit as st
from dynamicserialize import adapters , dstypes, DynamicSerializationManager, SelfDescribingBinaryProtocol , ThriftSerializationContext


def main():
    st.title("Dynamic serialization")

    exception_wrapper = 