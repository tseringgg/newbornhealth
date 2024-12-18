// In a service class
public class ChatbotService
{
    private readonly OpenAIClient _openAIClient;

    public ChatbotService(OpenAIClient openAIClient)
    {
        _openAIClient = openAIClient;
    }

    // Methods to interact with OpenAI
}