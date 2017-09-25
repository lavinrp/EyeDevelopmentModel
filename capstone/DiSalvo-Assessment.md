# Joe DiSalvo Capstone Essay

The rules by which fruit fly eyes develop are well-known, but the
rules by which the eyes of other animals develop are not. We will
create a simulation of fruit fly eye development that lets the user
vary biological constraints such as eye size to resemble other
animals. If the resulting eye is similar to that animals eye, then we
know that their eye development follows rules similar to the fruit
fly. If the simulation differs, we'll know that the animal follows
different developmental rules. Simulations of the biological
mechanisms by which fruit fly eyes form exist, but they are too
concerned with biological messaging to model the development of the
entire eye. We seek to build a higher-level simulation.

Programming Languages, Software Engineering, and D&A of Algorithms
will be helpful. From Programming Languages we get our spiritual
inspiration from functional languages -- wouldn't it be nice if we
could live in them. Our simulation might rely heavily on concurrency,
and thinking about how we would solve the problem in Clojure with
software transactional memory and immutable datastructures will make
our solution in Python cleaner probably. We'll use what we learned
about agile development and requirements engineering in Software
Engineering to figure out what our stakeholders actually want, and
iterate closer towards it. If we tried approaching this project with
an adhoc methodology, we would fail to deliver, because the
requirements take a lot of work to engineer and our first drafts are
likely to be very imperfect. D&A of Algorithms taught of how to
find/create efficient algorithms, which will be important since we
need our simulation to be performant.

As a developer co-op at Projetech, I learned how to elicit
requirements and handle a large code base. My team at Projetech did an
awful job eliciting requirements -- we did several months of
unnecessary work and built grandiose abstractions to solve problems
that didn't matter. We misunderstood the stakeholders' needs and
relied on speculation. But towards the end, we realized our errors and
got good at eliciting requirements and releasing in rapid iterations
to get frequent feedback, which greatly sped up the project. The
project started my first co-op and ended my fourth, so I got to see
how code I wrote at the beginning that seemed fine grew problematic as
the project grew, and learned the value/necessity of frequent
refactoring. I'm more sensitive to modular design now, since I've seen
what types of decisions come back to harm people in the future. An
aside: I also got over my discomfort of eating in public on the co-op,
and heard that the neurobiology professor we're developing this for
might give us smoked salmon and bagels, which I will now be able to
eat without feeling awkward.

I joined the project because I wanted to learn about something I never
thought I would learn about (fruit fly eye development and
simulations), and work with people I didn't know. So far, the biology
of eye development is fascinating. I hope to learn enough about eye
development to use that knowledge in an improv scene should I be
endowed as an eye doctor (8 months of work for 2 minutes of funny;
worth it). I wanted to work with people I didn't know because I never
really got to my know classmates, and it's better late than never. Although
my natural inclination is to work alone, I would benefit a lot from working
with people who have different co-op experiences from me and bring different
types of knowledge to the table. I'm hoping to learn about new programming
techniques, new algorithms, and new design/management methodologies.

The project is potentially endless; in the best of all worlds, the
simulation would be three dimensional and the cells would have
realistic, differing shapes and sizes. Our preliminary approach is to
make the simulation two dimensional and have every cell be a circle
(because collisions that result from e.g. cell division are easier to
handle). I expect that we can have a two dimensional, all-circle
simulation working by the end of the year. This would be a solid
foundation that other students or researchers could expand upon. We
will rely on Dr. Bushbeck (the neurobiology professor) to validate our
simulation and tell us whether we've done a good job, as she is the
domain expert. I consider a fully working 2D simulation, where
"working" means the biology checks out according to Dr. Bushbeck, a
good job, even if it's incomplete, since we have limited time and
(unpaid) labor to put into the project.
