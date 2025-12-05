# Contributing to LLM-Based DBMS

Thank you for your interest in contributing to the LLM-Based Database Management System project!

## Academic Context

This is an academic research project conducted at **Eskişehir Technical University**, Department of Electrical and Electronics Engineering, as part of the 2025-2026 Design Project curriculum and supported by TÜBİTAK 2209-A.

## Project Team

- **Derya Umut Kulalı** - Principal Investigator / Project Lead
- **Anıl Aydın** - Research Team Member
- **Sıla Alhan** - Research Team Member
- **Mehmet Fidan** - Academic Advisor

## How to Contribute

### Reporting Issues

If you find bugs or have feature requests:
1. Check if the issue already exists in the issue tracker
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant labels

### Development Setup

1. **Fork and Clone**
 ```bash
 git clone https://github.com/Japyh/llm-based-dbms.git
 cd llm-based-dbms
 ```

2. **Create Virtual Environment**
 ```bash
 python -m venv venv
 # Windows
 .\venv\Scripts\activate
 # Linux/macOS
 source venv/bin/activate
 ```

3. **Install Dependencies**
 ```bash
 pip install -r requirements-minimal.txt
 pip install -e ".[dev]" # Install dev dependencies
 ```

4. **Initialize Database**
 ```bash
 python scripts/init_db.py
 ```

5. **Run Tests**
 ```bash
 pytest backend/tests/ -v
 ```

### Code Style

This project follows:
- **PEP 8** for Python code style
- **Black** for code formatting (line length: 100)
- **isort** for import sorting
- **Type hints** for all function signatures
- **Docstrings** for all public functions and classes

Run linters before submitting:
```bash
black backend/
isort backend/
ruff check backend/
mypy backend/
```

### Making Changes

1. **Create a Branch**
 ```bash
 git checkout -b feature/your-feature-name
 ```

2. **Make Your Changes**
 - Write clear, concise commit messages
 - Add tests for new features
 - Update documentation as needed

3. **Test Your Changes**
 ```bash
 pytest backend/tests/ -v --cov=backend
 ```

4. **Commit and Push**
 ```bash
 git add .
 git commit -m "feat: add your feature description"
 git push origin feature/your-feature-name
 ```

5. **Create Pull Request**
 - Provide clear description of changes
 - Reference any related issues
 - Ensure CI passes

### Commit Message Format

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Build/config changes

Example:
```
feat: add support for PostgreSQL full-text search
```

### Testing Guidelines

- Write unit tests for all new functions
- Integration tests for API endpoints
- Ensure >80% code coverage
- Test both success and error cases
- Mock external dependencies (LLM APIs)

### Documentation

When adding features:
- Update relevant `.md` files in `docs/`
- Add docstrings to all new functions
- Update API reference if adding endpoints
- Include usage examples

### Areas for Contribution

#### High Priority
- [ ] Expand test coverage
- [ ] Add support for more SQL databases (MySQL, MariaDB)
- [ ] Implement column-level RBAC
- [ ] Add query result caching strategies

#### Medium Priority
- [ ] Create web-based UI (React/Next.js)
- [ ] Add support for local LLM providers (Ollama, vLLM)
- [ ] Implement multi-turn conversation context
- [ ] Add semantic search for schema documentation

#### Low Priority
- [ ] Performance profiling and optimization
- [ ] Add support for more LLM providers
- [ ] Implement query explanation visualization
- [ ] Add support for query history analytics

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

### Questions?

For questions about:
- **Technical Implementation**: Open an issue on GitHub
- **Academic Collaboration**: Contact the project team through Eskişehir Technical University
- **TÜBİTAK Project**: Refer to official TÜBİTAK 2209-A documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

We appreciate all contributions that help advance natural language interfaces for database systems and support the academic research goals of this project.
