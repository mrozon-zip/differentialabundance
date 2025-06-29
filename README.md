# 📓 Development Log – nf-core/differentialabundance Challenge

This log documents my process for developing small NextFlow and streamlit app. This log also includes detailed instructions on how to run the app, both the pipeline and the Streamlit interface. The project included modifying the `nf-core/differentialabundance` pipeline, customizing its output report, and developing a Dockerized Streamlit app for interactive visualization of DESeq2 and GSEA results. The app supports keyword-based search, result filtering, multi-page display, annotation integration, interactive plots, and Docker deployment.

---

## ▶️ Running the Streamlit App

1. There are two components of the application:
   - The **modified differentialabundance pipeline** (in the `differentialabundance` folder)
   - The **Streamlit web app** for result visualization (in the `streamlit_app` folder)

2. To run the pipeline, use:
   ```
   nextflow run main.nf -profile test_full,docker -outdir &lt;OUTDIR&gt;
   ```

3. This will generate a `report.html` file containing pipeline results with the requested customizations.

4. The Streamlit web app is available as a Docker image:
   ```
   docker pull mrozonzip/streamlit-app:2.0
   docker run -p 8501:8501 mrozonzip/streamlit-app:2.0
   ```
   Also available at: [Docker Hub - mrozonzip/streamlit-app](https://hub.docker.com/repository/docker/mrozonzip/streamlit-app/general)

5. The web app includes:
   - **Main page:** Select a directory containing the results of the pipeline.
   - **GSEA results page:** View GSEA tables and interactive dot plots.
   - **DESeq2 results page:** View DESeq2 tables and interactive volcano plots.

6. Once the correct folder is selected on the main page, the other pages can be used to explore visualizations and data summaries.

---

## 🧠 Overview

**Start Date:** 2025-06-23  
**Deadline:** ~1 week  
**Challenge Summary:**

- Nextflow usage and modification
  - Fix broken `test_full` profile in `nf-core/differentialabundance`
  - Modify the R Markdown report with:
    - GSEA: FDR < 0.25 cutoff, merge UP/DOWN tables
    - DESeq2: padj < 0.05 & |FC| > 1.3 cutoff, merge UP/DOWN, tag comparisons
- Build a Dockerized Streamlit app to visualize DESeq2 and GSEA results

---

## 📅 Log

### ✅ 2025-06-23 – Project Setup
- Forked and cloned `nf-core/differentialabundance` v1.5.0
- Skimmed docs and familiarized myself with the pipeline layout
- Created initial structure:
```
PCR_simulation/
│
├── /nextflow_workflow/         # modified pipeline
├── /streamlit_app/             # interactive dashbord
└── support.py README.md        # this log
```


### ✅ 2025-06-25 – Pipeline Profile & Local Execution Troubleshooting
- **Challenge:** `test_full` profile blew up with “matrix file not found.”  
  **Cause:** In `test_full.config`, the sample matrix file was referred to as `.txt` although the test data is shipped as `.tsv`.  
  **Solution:** Updated the extension in `test_full.config` from `.txt` → `.tsv`, and the full test now passes.

- **Challenge:** Running `nextflow run nf-core/differentialabundance` didn’t pick up local changes.  
  **Cause:** That command fetched the remote release pipeline instead of my fork.  
  **Solution:** Switched to `nextflow run main.nf …` (the local working copy) so edits were applied.

- **Challenge:** Identifying which file generates the HTML report.  
  **Cause:** It was unclear where the HTML output is defined in the pipeline.  
  **Solution:** Used an LLM and existing instructions to confirm that the `.Rmd` file renders the HTML report.

- **Challenge:** Applying the FDR < 0.25 cutoff to GSEA results without errors.  
  **Cause:** Filtering with `dplyr` resulted in errors, and column names did not align for programmatic subset.  
  **Solution:** Leveraged `subset()` addressing the FDR column by its index:  
  ```r
  target_gsea_results <- subset(target_gsea_results, target_gsea_results[[6]] < 0.25)
  ref_gsea_results <- subset(ref_gsea_results, ref_gsea_results[[6]] < 0.25)
  ```

### ✅ 2025-06-26
- **Goal:** Merge upregulated and downregulated DEGs into unified tables.
- **Challenge:** The original output displayed UP and DOWN genes in separate tables.
- **Solution:** Updated the `.Rmd` report logic:
  - Applied cutoff: `padj < 0.05` and `|log2FC| > log2(1.3)`
  - Combined filtered UP (logFC > 0) and DOWN (logFC < 0) genes into a single table per contrast.
  - Added columns: `Direction` ("UP"/"DOWN") and `Comparison` (e.g. "treated vs control in X").

### ✅ 2025-06-27
- Built a Streamlit app that searches for local files from `differentialabundance`, based on a predefined template.
- App capable of outputting result tables.
- Implemented functionality to search for files using keywords across folders in `../differentialabundance/test/report/`.
- Added new features:
  - Multiple pages for displaying results: main page, GSEA results, and DESeq2 results.
  - Interactive volcano plot for DESeq2 results.
  - Dot plot for GSEA results.

### ✅ 2025-06-28
- Replaced `matplotlib` with `plotly` to improve interactivity of plots.
- Enhanced display text to make file selection more intuitive.
- Added sorting options for GSEA plots.
- Integrated gene annotations into volcano plot using the annotation table.

### ✅ 2025-06-29
- Implemented file selection feature on the main page of the app.
- Verified successful deployment and function of the app as a Docker container.