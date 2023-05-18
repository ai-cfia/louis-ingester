import indexer as index_module

model = index_module.CohereModel()
model_index = index_module.get_index(model.index_name())
print(model_index.describe_index_stats())

query = "Find founding acts for organizations created by the government"

# create the query vector
xq = model.encode(query)
# print(xq)
# now query
xc = model_index.query(xq, top_k=5, include_metadata=True)
print(xc)