import click

from queueing import simulation
from distribute.uniform import UniformDistributon
from distribute.gaussian import GaussianDistributon

@click.command()
@click.option('--uniraw', prompt='Arguments for uniform distribution (separate by space)', help='Arguments for uniform distribution separated by space.')
@click.option('--gaussraw', prompt='Mean and variance for Gaussian distribution (separate by space)', help='Arguments for Gaussian distribution separated by space.')
@click.option('--jobs', prompt='Amount of jobs in queue', help='Amount of jobs in queue.', type=int)
@click.option('--prob', prompt='Probability of job returning in queue (percentage)', help='Probability of job returning in queue (in percentage).', type=float)
@click.option('--delta', prompt='Time delta for event simulation', help='Time delta for event simulation.', type=float)

def main(uniraw, gaussraw, jobs, prob, delta):

    uniformArgs = [f(i) for f,i in zip((float, float), uniraw.split())]
    if len(uniformArgs) != 2:
        click.echo("Invalid number of arguments for uniform distribution. Aborting...")
        return

    gaussArgs = [f(i) for f,i in zip((float, float), gaussraw.split())]
    if len(gaussArgs) != 2:
        click.echo("Invalid number of arguments for Gaussian distribution. Aborting...")
        return

    distribution = UniformDistributon(uniformArgs[0], uniformArgs[1])

    jobProcessor = GaussianDistributon(gaussArgs[0], gaussArgs[1])

    jobsAmount = jobs

    repeat_percentage = prob
    step = delta

    maxQueueLen, processedJobs, returnedJobs = simulation.TimekeepingSimulation(distribution, jobProcessor, jobsAmount, repeat_percentage, step)

    click.secho("TIME-KEEPING SIMULATION", fg='red', bold=True)
    click.secho(f"Maximum buffer capacity without losses: {maxQueueLen}", fg='red')
    click.secho(f"Number of processed jobs: {processedJobs}", fg='red')
    click.secho(f"Number of jobs re-entering buffer: {returnedJobs}", fg='red')

    maxQueueLen, processedJobs, returnedJobs = simulation.EventSimulation(distribution, jobProcessor, jobsAmount, repeat_percentage)

    click.secho("EVENT SIMULATION", fg='blue', bold=True)
    click.secho(f"Maximum buffer capacity without losses: {maxQueueLen}", fg='blue')
    click.secho(f"Number of processed jobs: {processedJobs}", fg='blue')
    click.secho(f"Number of jobs re-entering buffer: {returnedJobs}", fg='blue')

    
    # click.secho(f"Number of ")
    # click.echo(step_data)


if __name__ == '__main__':
    main()
    # print(uniRaw)