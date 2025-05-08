import { 
    Carousel,
    CarouselContent,
    CarouselItem,
} from "@/components/ui/carousel";
import QuestionCard from "./questionCard";

interface QuestionCarouselProps {
    questions: Array<{
        question: string;
        choices: string[];
        qtype: string;
        questionId: string;
        questionAnswer: string;
    }>;
}

export default function QuestionCarousel({ questions }: QuestionCarouselProps) { 
    
    return (
        <Carousel>
            <CarouselContent>
                {/* Iterate over your questions here*/}
                {questions.map((question) => (
                    <CarouselItem key={question.questionId} className="basis-1/3">
                        <QuestionCard
                            question={question.question}
                            choices={question.choices}
                            qtype={question.qtype}
                            questionId={question.questionId}
                            questionAnswer={question.questionAnswer} 
                        />                
                    </CarouselItem>
                ))}
            </CarouselContent>
        </Carousel>
    );
}
