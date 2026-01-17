# Testing Guide

## Unit Tests

### Backend Services

#### Run Product Service Tests
```bash
cd services/product-service
pip install -r requirements.txt
pytest tests/
```

#### Run Cart Service Tests
```bash
cd services/cart-service
pip install -r requirements.txt
pytest tests/
```

#### Run Auth Service Tests
```bash
cd services/auth-service
pip install -r requirements.txt
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm install
npm test
```

## Integration Tests

```bash
# Run all services
docker-compose up -d

# Run integration tests
pytest integration_tests/
```

## End-to-End Tests

### Prerequisites
- All services running
- Frontend built

```bash
cd frontend
npm install
npm run test:e2e
```

## Performance Testing

### Load Testing with Locust

```bash
# Install Locust
pip install locust

# Run load tests
locust -f tests/load_tests.py --host=http://localhost:8000
```

### API Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 100 http://localhost:8000/products

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/products
```

## Test Coverage

### Generate Coverage Report
```bash
pytest --cov=app tests/
```

### View HTML Report
```bash
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html
```

## Continuous Integration

### GitHub Actions

Tests are automatically run on:
- Push to main/develop
- Pull requests

See `.github/workflows/` for CI configuration.

## Test Data

### Seed Database
```bash
python scripts/seed_data.py
```

### Reset Database
```bash
python scripts/reset_db.py
```

## Debugging Tests

### Run with Verbose Output
```bash
pytest -v tests/
```

### Run Single Test
```bash
pytest tests/test_auth.py::test_login -v
```

### Use pdb Debugger
```python
def test_example():
    import pdb; pdb.set_trace()
    # Test code here
```

## Best Practices

1. Write tests for new features
2. Maintain >80% code coverage
3. Run tests before committing
4. Use descriptive test names
5. Mock external dependencies
6. Test both happy paths and error cases
7. Keep tests independent
8. Use fixtures for common setup
