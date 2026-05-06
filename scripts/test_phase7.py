"""Quick validation for Phase 7 observability modules."""

from backend.observability.tracing import get_langfuse, get_langfuse_handler, observe

# Since .env has placeholder keys 'sk-lf-changeme', it should attempt to init
client = get_langfuse()
assert client is not None, 'Client should instantiate with placeholder keys'

handler = get_langfuse_handler()
assert handler is not None, 'Handler should instantiate with placeholder keys'

@observe()
def dummy_traced_function():
    return 'ok'

print('tracing.py — ALL CHECKS PASSED')
