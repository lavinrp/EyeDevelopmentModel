# Professional Biography for Joe DiSalvo

# Contact Information
disalvjn@mail.uc.edu

# Co-op Work Experience
## Co-op Developer at Projetech -- Fall 2015 to Present
- A full time employee, me, and several other co-ops developed an internal autmation tool from scratch in Clojure (a functional LISP for the JVM).
### Programming
The automation tool had one central server - which had a REST API, access to a relational database, and a front-end - and multiple worker servers that received automation jobs from the central server. I wrote code for every part of the project; this includes schema design, SQL queries, REST endpoints, back-end server code, front-end code, and communication protocols between the central server and worker servers.

I also worked on a DSL in Clojure for expressing automation jobs as directed graphs, where the nodes are tasks and the edges represent dependencies between them. I implemented a declarative, constraint-based method to insert new tasks into the graph by specifying their relations to other nodes (e.g., Z comes after X but before Y; or Z comes after X and the job satisfies P). I also implemented the execution model using Clojure's software transactional memory; the execution model contained actions such as rolling back to a task, skipping over some tasks, and force starting a task even when its dependencies have not been met.

### Eliciting Requirements and Design
The early phases of the project were plauged by ambiguous requirements and unnecessary abstractions. We did several months of useless work, implementing features no one wanted, designing convoluted schemas to account for edge cases that didn't exist, and solving invented problems. I became more involved in requirements elicitation and design discussions. I developed clearer requirements by asking a lot of questions (often the requirements that people give you are actually proposed solutions to unstated requirements), and advocated for starting with simpler, minimalistic designs, getting frequent feedback, and iterating towards perfection. By the end of the project, I was responsible for the majority of design decisions, and functionally lead the other co-ops because the full time employee was pulled away from the project.

# Side Projects
## Library for Declarative Data Transformations in Clojure
I wrote a DSL for generating functions that transform nested data structures into other ones. For example, to generate a function to invert a map, you would write (transformer {k v} {v k}), which can be read as "transform a map from keys k to values v into a map from keys v to values k." If the values in the map are vectors, you would write (transformer {k [v]} {v k}). To index a vector of first-name, last-name records by first-name, you would write (transformer [{:first-name f, :last-name l}] {f #{l}}), which reads "transform a vector of records with first-names f and last-names l into a map from first-names to the set of corresponding last-names." We used this library at work.

https://github.com/disalvjn/faconne

## Compiler Self Study
I studied Andrew Appel's "Modern Compiler Implementation in Standard ML" and wrote a compiler for the simple, imperative language Tiger described in it. I used Haskell to implement it.
https://github.com/disalvjn/tiger-compiler

# Project Sought
