# Contributing to Job Apply Agent

Thank you for your interest in contributing! Here's how you can help.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for dev tools
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python
- Follow PEP 8
- Use type hints where possible
- Run `black` for formatting: `black app/`
- Run `flake8` for linting: `flake8 app/`

### TypeScript/JavaScript
- Use Prettier for formatting
- Follow ESLint rules
- Use TypeScript strict mode

## Testing

### Backend
```bash
pytest backend/tests/
```

### Frontend
```bash
npm test
```

## Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new job scraper for LinkedIn`
- `fix: Resolve resume parsing issue`
- `docs: Update API documentation`
- `refactor: Simplify authentication flow`

## Pull Request Process

1. Update the README.md if needed
2. Update ROADMAP.docx with new features/fixes
3. Ensure all tests pass
4. Request review from maintainers
5. Address feedback and push updates

## Areas for Contribution

- **New Job Board Scrapers**: Add support for LinkedIn, Indeed, Lever, etc.
- **Frontend Improvements**: Better UI/UX for dashboard and job tracking
- **Testing**: Add unit and integration tests
- **Documentation**: Improve guides and API documentation
- **Bug Fixes**: Found a bug? Please report it!
- **Performance**: Optimize scraping and API responses

## Reporting Issues

- Use GitHub Issues to report bugs
- Include steps to reproduce
- Specify your OS, Python version, and Node version
- Include error messages and logs

## Questions?

- Check existing issues and discussions
- Open a new discussion for questions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
