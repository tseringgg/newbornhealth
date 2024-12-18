// In a service class
public class CognitiveSearchService
{
    private readonly SearchClient _searchClient;

    public CognitiveSearchService(SearchClient searchClient)
    {
        _searchClient = searchClient;
    }

    // Methods to interact with Cognitive Search
}