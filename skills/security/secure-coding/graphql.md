# GraphQL Security

Introspection control, depth/complexity limits, batch abuse, field-level
authorization. GraphQL changes the threat model — one endpoint, many
shapes; rate limit by request count alone is insufficient.

Related: `express.md` (rate limiting baseline) · `auth.md`.

## Disable introspection in production

```javascript
// Apollo Server
const server = new ApolloServer({
  schema,
  introspection: process.env.NODE_ENV !== 'production',
  plugins: [
    process.env.NODE_ENV === 'production'
      ? ApolloServerPluginLandingPageDisabled()
      : ApolloServerPluginLandingPageLocalDefault()
  ]
});
```

```javascript
// express-graphql
const { NoIntrospection } = require('graphql');

app.use('/graphql', graphqlHTTP({
  schema: mySchema,
  validationRules: [NoIntrospection],
  graphiql: false
}));
```

## Query depth limiting

Without limits, attackers can send deeply nested queries that exponentially increase server load.

```javascript
const depthLimit = require('graphql-depth-limit');

app.use('/graphql', graphqlHTTP({
  schema: mySchema,
  validationRules: [depthLimit(5)]
}));
```

## Query complexity / cost analysis

```javascript
const { createComplexityLimitRule } = require('graphql-validation-complexity');

app.use('/graphql', graphqlHTTP({
  schema: mySchema,
  validationRules: [
    depthLimit(5),
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 10,
      listFactor: 20
    })
  ]
}));
```

## Batching attack prevention

GraphQL batching lets attackers send hundreds of queries in one HTTP request, bypassing per-request rate limits. Useful for brute-forcing OTPs, passwords, or enumeration.

```javascript
// Limit batch size
app.use('/graphql', (req, res, next) => {
  if (Array.isArray(req.body) && req.body.length > 5) {
    return res.status(400).json({ error: 'Batch limit exceeded' });
  }
  next();
});

// Apollo Server — disable batching entirely
const server = new ApolloServer({
  schema,
  allowBatchedHttpRequests: false
});
```

## Field-level authorization

```javascript
// WRONG: auth only on query resolver — any authenticated user sees any user's email/SSN
const resolvers = {
  Query: {
    user: (_, { id }, ctx) => {
      requireAuth(ctx);
      return db.users.findById(id);
    }
  },
  User: {
    email: (parent) => parent.email,
    ssn: (parent) => parent.ssn
  }
};

// CORRECT: auth on sensitive fields
const resolvers = {
  Query: {
    user: (_, { id }, ctx) => {
      requireAuth(ctx);
      return db.users.findById(id);
    }
  },
  User: {
    email: (parent, _, ctx) => {
      if (ctx.user.id !== parent.id && !ctx.user.isAdmin) {
        throw new ForbiddenError('Not authorized');
      }
      return parent.email;
    },
    ssn: (parent, _, ctx) => {
      if (!ctx.user.isAdmin) throw new ForbiddenError('Not authorized');
      return parent.ssn;
    }
  }
};
```

## Pentest checklist

- Send introspection query: `{__schema{types{name,fields{name}}}}`
- Try deeply nested queries (depth bomb)
- Try unbounded lists: `{ users(first:99999) { ... } }`
- Batch multiple queries in one request
- Alias the same field 1000 times: `{ a1: user(id:1){name} a2: user(id:2){name} ... }`
- Check for field suggestions in error messages (schema leakage without introspection)
- Test IDOR via direct ID access in queries/mutations
