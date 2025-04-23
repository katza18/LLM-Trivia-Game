import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

// Define the form schema using zod for validation
const formSchema = z.object({
    topic: z.string().min(4, {
        message: "Topic must be at least 4 characters long",
    }).max(50, {
        message: "Topic must be less than 50 characters long",
    }),
    qtype: z.enum(["multi", "short"]), // multiple choice or short answer
})


function Home(){
    const navigate = useNavigate();

    // Define the form
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            topic: "",
            qtype: undefined,
        },
    })

    // Define the submit handler
    function onSubmit(values: z.infer<typeof formSchema>) {
        console.log(values)
        navigate('/quiz', {state: values})
    }

    return (
        <div className="flex items-center justify-center flex-grow">
            <Card className="w-full max-w-md">
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)}>
                        <CardHeader>
                            <CardTitle>Generate a Quiz</CardTitle>
                            <CardDescription>Input a topic and select a question type to generate a quiz.</CardDescription>
                        </CardHeader>
                        <CardContent className='flex flex-col gap-4'>
                            <div className='flex flex-col gap-2'>
                                <FormField
                                    control={form.control}
                                    name="topic"
                                    render= {({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor="topic">Topic</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Input a quiz topic" {...field} />
                                            </FormControl>
                                            <FormDescription>Enter a topic for the quiz.</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                            <div className='flex flex-col gap-2'>
                                <FormField
                                    control={form.control}
                                    name="qtype"
                                    render= {({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor="qtype">Question Type</FormLabel>
                                            <FormControl>
                                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select a question type" />
                                                    </SelectTrigger>
                                                    <SelectContent>
                                                        <SelectItem value="multi">Multiple Choice</SelectItem>
                                                        <SelectItem value="short">Short Answer</SelectItem>
                                                    </SelectContent>
                                                </Select>
                                            </FormControl>
                                            <FormDescription>Select a question type for the quiz.</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button type="submit">Generate Quiz</Button>
                        </CardFooter>
                    </form>
                </Form>
            </Card>
        </div>
    )
}

export default Home;
