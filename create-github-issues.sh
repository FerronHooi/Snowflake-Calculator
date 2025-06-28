#!/bin/bash

# Script to create GitHub issues for Snowflake Calculator project completion
# Prerequisites: 
# 1. Enable GitHub Issues in repository settings
# 2. Have GitHub CLI (gh) installed and authenticated
# 3. Run: chmod +x create-github-issues.sh

echo "Creating GitHub issues for Snowflake Calculator completion..."

# Create labels first
echo "Creating labels..."
gh label create "high-priority" --color "D73A4A" --description "Critical issues that need immediate attention" 2>/dev/null || echo "Label high-priority already exists"
gh label create "medium-priority" --color "FFA500" --description "Important but not critical issues" 2>/dev/null || echo "Label medium-priority already exists"
gh label create "low-priority" --color "0E8A16" --description "Nice to have improvements" 2>/dev/null || echo "Label low-priority already exists"
gh label create "security" --color "D73A4A" --description "Security vulnerability or concern" 2>/dev/null || echo "Label security already exists"
gh label create "ui/ux" --color "7057FF" --description "User interface and experience improvements" 2>/dev/null || echo "Label ui/ux already exists"
gh label create "testing" --color "0969DA" --description "Testing related issues" 2>/dev/null || echo "Label testing already exists"
gh label create "performance" --color "FBCA04" --description "Performance improvements" 2>/dev/null || echo "Label performance already exists"

# Issue 1: Security - Remove hardcoded credentials
echo "Creating issue 1: Security - Remove hardcoded credentials..."
gh issue create --title "🔒 Security: Remove hardcoded API keys and Azure connection strings" \
--body "## Description
The application currently has hardcoded sensitive information that should be moved to environment variables or configuration files.

## Affected Files
- \`snowflake_scraper_timer_/__init__.py\`: Contains hardcoded Azure connection strings and Log Analytics credentials
- \`docs/index.html\`: Contains Exchange Rate API key directly in the source

## Tasks
- [ ] Create \`.env\` file structure for local development
- [ ] Implement environment variable loading in Azure Functions
- [ ] Update deployment documentation with required environment variables
- [ ] Add \`.env.example\` file with dummy values
- [ ] Update frontend to fetch API key from backend or use proxy

## Acceptance Criteria
- No sensitive information in source code
- All secrets managed through environment variables
- Documentation updated with configuration instructions" \
--label "bug" --label "security" --label "high-priority"

# Issue 2: Fix GBP currency support
echo "Creating issue 2: Fix GBP currency support..."
gh issue create --title "💷 Fix GBP currency support" \
--body "## Description
GBP currency option exists but has empty string values in the pricing data, making it non-functional.

## Tasks
- [ ] Investigate why GBP values are empty in SnowflakeCloudData.json
- [ ] Update scraper to properly fetch GBP pricing
- [ ] Add fallback calculation from USD if direct GBP pricing unavailable
- [ ] Test all calculations with GBP currency

## Acceptance Criteria
- GBP currency fully functional
- All pricing tiers show correct GBP values
- Currency conversion works if needed" \
--label "bug" --label "high-priority"

# Issue 3: Add error handling for failed API calls
echo "Creating issue 3: Add error handling for failed API calls..."
gh issue create --title "⚠️ Add error handling for failed API calls" \
--body "## Description
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
- Calculator remains functional with cached data" \
--label "bug" --label "enhancement" --label "high-priority"

# Issue 4: Create comprehensive README documentation
echo "Creating issue 4: Create comprehensive README documentation..."
gh issue create --title "📚 Create comprehensive README documentation" \
--body "## Description
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
- License" \
--label "documentation" --label "high-priority"

# Issue 5: Implement proper package management
echo "Creating issue 5: Implement proper package management..."
gh issue create --title "📦 Implement proper package management" \
--body "## Description
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
- Build process documented" \
--label "enhancement" --label "high-priority"

# Issue 6: Add input validation and sanitization
echo "Creating issue 6: Add input validation and sanitization..."
gh issue create --title "✅ Add input validation and sanitization" \
--body "## Description
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
- No security vulnerabilities from user input" \
--label "bug" --label "security" --label "high-priority"

# Issue 7: Improve mobile responsiveness
echo "Creating issue 7: Improve mobile responsiveness..."
gh issue create --title "📱 Improve mobile responsiveness" \
--body "## Description
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
- No horizontal overflow on small screens" \
--label "enhancement" --label "ui/ux" --label "medium-priority"

# Issue 8: Add dark mode support
echo "Creating issue 8: Add dark mode support..."
gh issue create --title "🌙 Add dark mode support" \
--body "## Description
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
- All elements properly styled in both modes" \
--label "enhancement" --label "ui/ux" --label "medium-priority"

# Issue 9: Improve PDF export formatting
echo "Creating issue 9: Improve PDF export formatting..."
gh issue create --title "📄 Improve PDF export formatting" \
--body "## Description
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
- Customizable export options" \
--label "enhancement" --label "ui/ux" --label "medium-priority"

# Issue 10: Set up automated testing framework
echo "Creating issue 10: Set up automated testing framework..."
gh issue create --title "🧪 Set up automated testing framework" \
--body "## Description
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
- UI interactions: 80%" \
--label "testing" --label "enhancement" --label "medium-priority"

# Issue 11: Add data validation for scraped pricing
echo "Creating issue 11: Add data validation for scraped pricing..."
gh issue create --title "🔍 Add data validation for scraped pricing" \
--body "## Description
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
- Historical pricing data available" \
--label "testing" --label "enhancement" --label "medium-priority"

# Issue 12: Implement caching strategy
echo "Creating issue 12: Implement caching strategy..."
gh issue create --title "💾 Implement caching strategy" \
--body "## Description
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
- Cache updates handled smoothly" \
--label "enhancement" --label "performance" --label "low-priority"

# Issue 13: Optimize asset loading
echo "Creating issue 13: Optimize asset loading..."
gh issue create --title "⚡ Optimize asset loading" \
--body "## Description
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
- Reduced bundle size by 30%" \
--label "enhancement" --label "performance" --label "low-priority"

echo "✅ All issues created successfully!"
echo "View them at: https://github.com/FerronHooi/Snowflake-Calculator/issues"