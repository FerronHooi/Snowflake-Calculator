# Snowflake Calculator - Website Completion Plan

## Overview
This document outlines the comprehensive plan to finish the Snowflake Calculator website. The issues are organized by priority and category.

## Prerequisites
1. Enable GitHub Issues for the repository (Settings → Features → Issues)
2. Create appropriate labels: `bug`, `enhancement`, `documentation`, `security`, `high-priority`, `medium-priority`, `low-priority`, `testing`, `ui/ux`

## GitHub Issues to Create

### 🔴 Critical Issues (High Priority)

#### 1. Security: Remove hardcoded API keys and Azure connection strings
**Labels:** `bug`, `security`, `high-priority`
```markdown
## Description
The application currently has hardcoded sensitive information that should be moved to environment variables or configuration files.

## Affected Files
- `snowflake_scraper_timer_/__init__.py`: Contains hardcoded Azure connection strings and Log Analytics credentials
- `docs/index.html`: Contains Exchange Rate API key directly in the source

## Tasks
- [ ] Create `.env` file structure for local development
- [ ] Implement environment variable loading in Azure Functions
- [ ] Update deployment documentation with required environment variables
- [ ] Add `.env.example` file with dummy values
- [ ] Update frontend to fetch API key from backend or use proxy

## Acceptance Criteria
- No sensitive information in source code
- All secrets managed through environment variables
- Documentation updated with configuration instructions
```

#### 2. Fix GBP currency support
**Labels:** `bug`, `high-priority`
```markdown
## Description
GBP currency option exists but has empty string values in the pricing data, making it non-functional.

## Tasks
- [ ] Investigate why GBP values are empty in SnowflakeCloudData.json
- [ ] Update scraper to properly fetch GBP pricing
- [ ] Add fallback calculation from USD if direct GBP pricing unavailable
- [ ] Test all calculations with GBP currency

## Acceptance Criteria
- GBP currency fully functional
- All pricing tiers show correct GBP values
- Currency conversion works if needed
```

#### 3. Add error handling for failed API calls
**Labels:** `bug`, `enhancement`, `high-priority`
```markdown
## Description
When the Exchange Rate API or pricing data API fails, users see no feedback and calculations may fail silently.

## Tasks
- [ ] Add try-catch blocks around all API calls
- [ ] Display user-friendly error messages
- [ ] Implement retry logic for transient failures
- [ ] Add fallback to cached exchange rates
- [ ] Show loading indicators during API calls

## Acceptance Criteria
- All API failures handled gracefully
- Users see clear error messages
- Calculator remains functional with cached data
```

### 🟡 Core Features (High Priority)

#### 4. Create comprehensive README documentation
**Labels:** `documentation`, `high-priority`
```markdown
## Description
Project lacks README.md with setup instructions, usage guide, and contribution guidelines.

## Tasks
- [ ] Create README.md with project overview
- [ ] Add installation instructions for local development
- [ ] Document Azure Functions deployment process
- [ ] Include API documentation
- [ ] Add contribution guidelines
- [ ] Include screenshots of the calculator

## Sections to Include
- Project Overview
- Features
- Prerequisites
- Installation
- Configuration
- Deployment
- API Documentation
- Contributing
- License
```

#### 5. Implement proper package management
**Labels:** `enhancement`, `high-priority`
```markdown
## Description
Project lacks package.json and proper dependency management.

## Tasks
- [ ] Create package.json with all frontend dependencies
- [ ] Set up npm scripts for common tasks
- [ ] Create requirements.txt for Python dependencies
- [ ] Document dependency installation process
- [ ] Consider using a bundler (webpack/vite) for production

## Acceptance Criteria
- All dependencies properly declared
- Single command to install all dependencies
- Build process documented
```

#### 6. Add input validation and sanitization
**Labels:** `bug`, `security`, `high-priority`
```markdown
## Description
Calculator inputs lack proper validation which could lead to calculation errors or security issues.

## Tasks
- [ ] Validate numeric inputs (storage, hours, percentage)
- [ ] Set min/max limits for all inputs
- [ ] Sanitize warehouse names to prevent XSS
- [ ] Validate currency and region selections
- [ ] Show validation errors to users

## Acceptance Criteria
- All inputs validated before calculation
- Clear error messages for invalid inputs
- No security vulnerabilities from user input
```

### 🟢 UI/UX Improvements (Medium Priority)

#### 7. Improve mobile responsiveness
**Labels:** `enhancement`, `ui/ux`, `medium-priority`
```markdown
## Description
Calculator interface needs optimization for mobile devices.

## Tasks
- [ ] Add viewport meta tag if missing
- [ ] Make sliders touch-friendly
- [ ] Adjust layout for small screens
- [ ] Test on various device sizes
- [ ] Optimize button sizes for touch
- [ ] Make tables horizontally scrollable

## Acceptance Criteria
- Calculator fully functional on mobile
- All elements properly sized for touch
- No horizontal overflow on small screens
```

#### 8. Add dark mode support
**Labels:** `enhancement`, `ui/ux`, `medium-priority`
```markdown
## Description
Add toggle for dark mode to improve user experience.

## Tasks
- [ ] Create dark color scheme
- [ ] Add theme toggle button
- [ ] Save user preference in localStorage
- [ ] Update all UI elements for dark mode
- [ ] Ensure PDF export works with both themes

## Acceptance Criteria
- Smooth theme switching
- User preference persisted
- All elements properly styled in both modes
```

#### 9. Improve PDF export formatting
**Labels:** `enhancement`, `ui/ux`, `medium-priority`
```markdown
## Description
PDF export needs better formatting and professional appearance.

## Tasks
- [ ] Add company branding to PDF header
- [ ] Format tables properly in PDF
- [ ] Include calculation parameters in export
- [ ] Add page numbers and date
- [ ] Optimize for A4/Letter paper sizes
- [ ] Add option to include/exclude sections

## Acceptance Criteria
- Professional-looking PDF exports
- All data clearly formatted
- Customizable export options
```

### 🔵 Testing & Quality (Medium Priority)

#### 10. Set up automated testing framework
**Labels:** `testing`, `enhancement`, `medium-priority`
```markdown
## Description
Project needs comprehensive testing to ensure reliability.

## Tasks
- [ ] Set up Jest for frontend JavaScript testing
- [ ] Create unit tests for calculation logic
- [ ] Set up pytest for Python Azure Functions
- [ ] Add integration tests for API endpoints
- [ ] Create E2E tests with Playwright/Cypress
- [ ] Set up GitHub Actions for CI/CD

## Test Coverage Goals
- Calculation logic: 100%
- API endpoints: 90%
- UI interactions: 80%
```

#### 11. Add data validation for scraped pricing
**Labels:** `testing`, `enhancement`, `medium-priority`
```markdown
## Description
Scraped pricing data should be validated to ensure accuracy.

## Tasks
- [ ] Add validation rules for pricing data structure
- [ ] Implement sanity checks (e.g., prices > 0)
- [ ] Alert when pricing changes significantly
- [ ] Add manual verification process
- [ ] Create pricing history tracking

## Acceptance Criteria
- Invalid data rejected automatically
- Alerts for unusual pricing changes
- Historical pricing data available
```

### ⚪ Performance & Optimization (Low Priority)

#### 12. Implement caching strategy
**Labels:** `enhancement`, `performance`, `low-priority`
```markdown
## Description
Reduce API calls and improve performance with proper caching.

## Tasks
- [ ] Cache exchange rates with TTL
- [ ] Cache pricing data locally
- [ ] Implement service worker for offline support
- [ ] Add cache invalidation strategy
- [ ] Monitor cache hit rates

## Acceptance Criteria
- Reduced API calls by 50%
- Calculator works offline with cached data
- Cache updates handled smoothly
```

#### 13. Optimize asset loading
**Labels:** `enhancement`, `performance`, `low-priority`
```markdown
## Description
Improve page load performance by optimizing assets.

## Tasks
- [ ] Minify CSS and JavaScript
- [ ] Optimize images (compress, WebP format)
- [ ] Implement lazy loading for images
- [ ] Bundle JavaScript modules
- [ ] Add resource hints (preconnect, prefetch)
- [ ] Enable gzip compression

## Acceptance Criteria
- Page load time < 2 seconds
- Lighthouse score > 90
- Reduced bundle size by 30%
```

## Execution Order

1. **Week 1-2:** Critical Security & Bug Fixes (Issues 1-3)
2. **Week 3-4:** Documentation & Setup (Issues 4-5)
3. **Week 5-6:** Core Features (Issue 6) & Initial Testing (Issue 10)
4. **Week 7-8:** UI/UX Improvements (Issues 7-9)
5. **Week 9-10:** Testing & Quality Assurance (Issue 11)
6. **Week 11-12:** Performance Optimization (Issues 12-13)

## Success Metrics

- Zero security vulnerabilities
- 100% currency support functional
- Mobile-responsive design
- Comprehensive documentation
- Automated test coverage > 80%
- Page load time < 2 seconds
- Error rate < 0.1%

## Next Steps

1. Enable GitHub Issues in repository settings
2. Create the labels mentioned above
3. Create each issue using the templates provided
4. Assign priorities and milestones
5. Begin execution starting with critical issues