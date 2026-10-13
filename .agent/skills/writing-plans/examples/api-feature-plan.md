# Example: API Feature Plan

```markdown
# User Authentication API Implementation Plan

**Goal:** Add JWT-based authentication with login, register, and token refresh.

**Architecture:** Express middleware validates tokens on protected routes.
Passwords hashed with bcrypt. Tokens issued and refreshed via dedicated
endpoints.

**Tech Stack:** Express, jsonwebtoken, bcrypt, Prisma ORM

**Spec:** docs/specs/2026-09-20-auth-design.md

## Global Constraints

- Node.js >= 20, TypeScript strict mode
- All endpoints return JSON with consistent error shape
- Passwords: bcrypt cost factor 12, never logged or returned

## Review Focus

- Empty string password should be rejected at validation, not at bcrypt
- Expired refresh token returns 401, not 500
- Concurrent token refresh with same token: second call fails gracefully
- SQL injection via email field in login
- Missing Content-Type header returns 415, not crash

---

### Task 1: User Model & Migration

**Files:**
- Create: `prisma/migrations/001_users/migration.sql`
- Create: `src/models/user.ts`
- Test: `tests/models/user.test.ts`

**Interfaces:**
- Consumes: nothing
- Produces: `createUser(email: string, passwordHash: string): Promise<User>`
            `findUserByEmail(email: string): Promise<User | null>`

- [ ] **Step 1: Write the failing test**

\`\`\`typescript
describe('User model', () => {
  it('creates a user and retrieves by email', async () => {
    const user = await createUser('test@example.com', 'hash123');
    const found = await findUserByEmail('test@example.com');
    expect(found?.email).toBe('test@example.com');
  });
});
\`\`\`

- [ ] **Step 2: Run test — expected FAIL**

Run: `npx jest tests/models/user.test.ts -v`
Expected: FAIL — createUser is not defined

- [ ] **Step 3: Create Prisma schema + model functions**

Add User model to schema.prisma, run migration, implement both functions.

- [ ] **Step 4: Run test — expected PASS**

Run: `npx jest tests/models/user.test.ts -v`
Expected: PASS 1/1

- [ ] **Step 5: Commit**

\`\`\`bash
git add prisma/ src/models/user.ts tests/models/user.test.ts
git commit -m "feat: add user model with create and findByEmail"
\`\`\`

### Task 2: Registration Endpoint
...
```
