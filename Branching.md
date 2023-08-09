### Branching Design

- **`main` branch:** This will be your production-ready code branch. Code in this branch should be stable and tested, as it represents what's deployed to your Production environment.
  
- **`dev` branch:** This is the branch for combined team development, integration, and initial testing. Code here will be deployed to a test instance in Azure.

- **Individual branches for developers:** `wikus` and `mari` branches. These branches are where each developer will primarily work on their tasks. Each developer branch is spawned from the `dev` branch and, once their work is complete and tested, will be merged back into it.

### Mermaid Diagram

Here's a simple diagram representing the branching structure:

:::mermaid
graph LR
    main(main) --> |Release| prod[Production]
    dev(dev) --> |Deploy| test[Test Azure Instance]
    wikus --> dev
    mari --> dev
:::

### Code Merging Plan

1. **Setting Up:**
   
   - Initialize your repository in Azure DevOps.
   - Create the `main` and `dev` branches.
   - Wikus and Mari can create their branches named `wikus` and `mari` respectively.<br><br>

2. **Regular Development Workflow:**

   - **Working Locally:** Wikus and Mari will clone the repo and work on their respective branches.
     
     ```bash
     git clone [REPO_URL]
     git checkout [branch_name]  # either 'wikus' or 'mari'
     ```

   - They can regularly commit and push changes to their branches:
     
     ```bash
     git add .
     git commit -m "Descriptive commit message"
     git push origin [branch_name]
     ```

   - When ready to integrate their work with the team's combined development (e.g., after completing a feature), they should:
     
     1. Ensure their branch has the latest changes from `dev`:

        ```bash
        git checkout [branch_name]  # switch to their branch if not already on it
        git pull origin dev
        ```

        Handle any merge conflicts if they arise.

     2. Push the merged changes to their branch:

        ```bash
        git push origin [branch_name]
        ```

     3. In Azure DevOps, open a Pull Request to merge their branch (`wikus` or `mari`) into the `dev` branch. This PR serves as an opportunity for code review and discussion.<br><br>

3. **Merging to `dev` and Deploying to Test:**

   - After reviewing the PR and ensuring there are no conflicts, you can merge it into the `dev` branch.
   - Deploy the `dev` branch to your test Azure instance for testing.<br><br>

4. **Promoting to Production:**

   - Once the `dev` branch is stable and you're ready to release to production:
     
     ```bash
     git checkout main
     git pull origin dev  # this merges dev into main
     git push origin main
     ```

   - Deploy the `main` branch to Production.<br><br>

5. **Regular Maintenance:**

   - Ensure that `dev` is regularly updated with `main` to keep it close to the production version, especially after every production release:

     ```bash
     git checkout dev
     git pull origin main
     git push origin dev
     ```

### Final Thoughts:

- Ensure Wikus and Mari are familiar with Git, especially resolving merge conflicts.
- It's advisable to have a CI/CD pipeline that runs tests automatically when PRs are opened. This ensures that changes don't introduce bugs.
- Keep communications open. If Wikus and Mari are working on interrelated components, they should coordinate to prevent major merge conflicts.
- Periodic code reviews, even before opening PRs, can be beneficial for maintaining code quality.