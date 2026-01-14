# Roadmap

This roadmap outlines potential next steps for evolving the platform into a
full AWS-based serverless solution.

## Phase 1: Local Stability

- [x] Deterministic local database initialization
- [x] API coverage for core flows
- [x] End-to-end smoke tests
- [x] CI pipeline for verification

## Phase 2: AWS Parity

- [ ] Swap SQLite for DynamoDB repositories
- [ ] Update Lambda handlers to use DynamoDB adapters
- [ ] Integrate Cognito for signup/login flows
- [ ] Introduce S3-backed storage for product images
- [ ] Add CloudWatch-based logging

## Phase 3: Production Hardening

- [ ] Add API rate limiting
- [ ] Implement per-user authorization guards
- [ ] Introduce order fulfillment workflow
- [ ] Add background recommendation jobs
- [ ] Add observability dashboards

## Phase 4: Frontend

- [ ] Build a React UI that consumes the API
- [ ] Implement cart and checkout UX
- [ ] Add server-side rendering for SEO

## Phase 5: Operations

- [ ] Add Terraform or CDK deployment scripts
- [ ] Add staging and production environments
- [ ] Add smoke tests against deployed stacks
- [ ] Add release automation
