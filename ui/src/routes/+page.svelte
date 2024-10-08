<script lang="ts">
    import { Card } from "@/components/ui/card";
    import { Input } from "@/components/ui/input";
    import { Label } from "@/components/ui/label";
    import { Button } from "@/components/ui/button";
    import LoaderCircle from "lucide-svelte/icons/loader-circle";
    import * as Select from "@/components/ui/select/index.js";
    import CardTitle from "@/components/ui/card/card-title.svelte";

    const languages = [
        { value: "pt", label: "Portuguese" },
        { value: "en", label: "English" },
        { value: "fr", label: "French" },
        { value: "es", label: "Spanish" },
        { value: "ja", label: "Japanese" },
        { value: "zh", label: "Chinese" },
    ];

    let video = "";
    let text = "";
    let language = "";
    let results: any[] = [];
    let error = "";
    let loading = false;
    $: isFormComplete =
        video.trim() !== "" && text.trim() !== "" && language.trim() !== "";

    function secondsToTimeFormat(seconds: number) {
        let date = new Date(0);
        date.setSeconds(seconds);
        const timeString = date.toISOString().substring(11, 19);
        return timeString;
    }
    async function handleSubmit(event: Event) {
        results = [];
        error = "";
        loading = true;
        event.preventDefault();

        try {
            const payload = {
                video: video,
                text: text,
                language: language,
            };

            const response = await fetch(`${import.meta.env.VITE_API_URL}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload), // Convert the payload to JSON
            });

            if (!response.ok) {
                loading = false;
                error = await response.text();
                return;
            }

            results = await response.json(); // Handle the response
            if (results.length == 0) {
                loading = false;
                error = "no text found";
                return;
            }
            loading = false;
        } catch (error) {
            loading = false;
            error = "failed to search for the text";
        }
    }
</script>

<div class="flex-1">
    <div class="container">
        <div
            class="w-full relative flex flex-col items-start md:flex-row md:items-center"
        >
            <section
                class="mx-auto flex max-w-[980px] flex-col items-center gap-2 py-8 md:py-12 md:pb-8 lg:py-24 lg:pg-20"
            >
                <h1
                    class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl"
                >
                    Quotube
                </h1>
                <p
                    class="text-muted-foreground max-w-[750px] text-center text-lg sm:text-xl"
                >
                    Search for Youtube video sections by it's subtitles
                </p>
            </section>
        </div>
        <form method="post" on:submit={handleSubmit}>
            <section
                class="mx-auto flex max-w-[500px] flex-col items-start gap-2 pt-8 md:py-12 md:pb-8 lg:py-3 lg:pg-20"
            >
                <Label for="video">Video Link</Label>
                <Input
                    type="text"
                    id="video"
                    placeholder=""
                    bind:value={video}
                    required
                />
                <p class="text-muted-foreground text-sm">
                    Enter the Youtube video link
                </p>
            </section>
            <section
                class="mx-auto flex max-w-[500px] flex-col items-start gap-2 py-2 md:py-12 md:pb-8 lg:py-3 lg:pg-20"
            >
                <Label for="text">Text</Label>
                <Input
                    type="text"
                    id="text"
                    placeholder=""
                    bind:value={text}
                    required
                />
                <p class="text-muted-foreground text-sm">
                    Enter the text to be searched
                </p>
            </section>
            <section
                class="mx-auto flex max-w-[500px] flex-row justify-between items-start gap-2 py-2 md:py-12 md:pb-8 lg:py-2 lg:pg-20"
            >
                <Select.Root
                    portal={null}
                    onSelectedChange={(v) => {
                        v && (language = v.value);
                    }}
                >
                    <Select.Trigger class="w-[180px]">
                        <Select.Value placeholder="Language" />
                    </Select.Trigger>
                    <Select.Content>
                        <Select.Group>
                            {#each languages as language}
                                <Select.Item
                                    value={language.value}
                                    label={language.label}
                                    >{language.label}</Select.Item
                                >
                            {/each}
                        </Select.Group>
                    </Select.Content>
                    <Select.Input name="favoriteFruit" />
                </Select.Root>

                <Button disabled={!isFormComplete || loading} type="submit">
                    {#if loading}
                        <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
                        Please wait
                    {:else}
                        Search
                    {/if}
                </Button>
            </section>
            <section
                class="mx-auto flex max-w-[500px] flex-col justify-between items-start gap-2 py-2 md:py-12 md:pb-8 lg:py-2 lg:pg-20"
            >
                {#each results as result}
                    <Card
                        class="mx-auto w-full flex-row flex justify-between p-4 items-center"
                    >
                        <h4
                            class="scroll-m-20 text-md font-semibold tracking-tight p-2"
                        >
                            <q>{result.text}</q>
                        </h4>
                        <Button
                            target="_black"
                            href={video + "&t=" + Math.trunc(result.start)}
                            >{secondsToTimeFormat(
                                Math.trunc(result.start),
                            )}</Button
                        >
                    </Card>
                {/each}
                {#if error}
                    <h3>Error: {error}</h3>
                {/if}
            </section>
        </form>
    </div>
</div>
