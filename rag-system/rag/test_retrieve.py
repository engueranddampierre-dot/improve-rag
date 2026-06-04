from rag.builder_code import retrieve_maude_context

code = open("tests/original/maudec/maude/stack2.maude").read()
print(retrieve_maude_context(code))