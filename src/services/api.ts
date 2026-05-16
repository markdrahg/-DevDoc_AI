const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface IngestionResponse {
  job_id: string;
  status: string;
  message: string;
  ingestion_type: string;
  created_at: string;
}

interface QueryResponse {
  answer: string;
  citations: Array<{
    file_path: string;
    line_start: number;
    line_end: number;
    content: string;
    relevance_score: number;
  }>;
  confidence: number;
  processing_time: number;
}

interface HealthCheckResponse {
  status: string;
  version: string;
  timestamp: string;
  ai_engine_status: string;
  uptime: number;
}

interface IngestionStatusResponse {
  job_id: string;
  status: string;
  progress: number;
  message: string;
  result?: {
    files_processed: number;
    total_files: number;
    repo_id?: string;
  };
  error?: string;
}

export const api = {
  // Health Check
  healthCheck: async (): Promise<HealthCheckResponse> => {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) throw new Error("Health check failed");
    return response.json();
  },

  // GitHub Ingestion
  ingestGitHub: async (
    repoUrl: string,
    branch: string = "main",
  ): Promise<IngestionResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/ingest/github`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl, branch }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(
        error.detail || error.message || "GitHub ingestion failed",
      );
    }
    return response.json();
  },

  // ZIP Ingestion
  ingestZip: async (file: File): Promise<IngestionResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/api/ingest/zip`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.message || "ZIP ingestion failed");
    }
    return response.json();
  },

  // PDF Ingestion
  ingestPdf: async (file: File): Promise<IngestionResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/api/ingest/pdf`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.message || "PDF ingestion failed");
    }
    return response.json();
  },

  // Check Ingestion Status
  getIngestionStatus: async (
    jobId: string,
  ): Promise<IngestionStatusResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/ingest/status/${jobId}`);
    if (!response.ok) throw new Error("Failed to get ingestion status");
    return response.json();
  },

  // Ask Question
  askQuestion: async (
    question: string,
    repoId?: string,
    maxResults: number = 5,
  ): Promise<QueryResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/query/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        repo_id: repoId,
        max_results: maxResults,
        include_citations: true,
      }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.message || "Query failed");
    }
    return response.json();
  },

  // Generate Documentation
  generateDocs: async (repoId: string, docType: string = "full") => {
    const response = await fetch(`${API_BASE_URL}/api/documentation/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        repo_id: repoId,
        doc_type: docType,
        include_diagrams: true,
      }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(
        error.detail || error.message || "Documentation generation failed",
      );
    }
    return response.json();
  },

  // Get Health Score
  getHealthScore: async (repoId: string) => {
    const response = await fetch(
      `${API_BASE_URL}/api/documentation/health/${repoId}`,
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(
        error.detail || error.message || "Failed to get health score",
      );
    }
    return response.json();
  },

  // Get Documentation
  getDocumentation: async (repoId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/documentation/${repoId}`);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(
        error.detail || error.message || "Failed to get documentation",
      );
    }
    return response.json();
  },
};

// Made with Bob
