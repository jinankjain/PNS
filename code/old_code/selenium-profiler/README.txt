The webprofiling uses selenium 1, an old version which allowed capturing network
traffic. To use it, run the standalone server (java -jar
selenium-server-standalone-2.53.1.jar), and install an old version of the python
selenium client (pip install selenium=1.0.3).

I got the code from https://code.google.com/archive/p/selenium-profiler

Notes and problems:
- Selenium can also be used with a java client, and online there are probably
  more solutions about how to work with the java version than with python.
- Right now, the script only returns the resource name, not the actual domain,
  and by looking into the code the server returns a local url, e.g.,
  http://localhost:4444/favicon.ico, so the original information is lost.
- NEXT STEP: my idea is to solve this by using selenium only to open the
  website, and let the request run over a proxy that we control, which could
  return, after every website loading, the list of GET request URLs that where
  accessed. There is the code for such a server at
http://www.jtmelton.com/2007/11/27/a-simple-multi-threaded-java-http-proxy-server/
- To just open a website, it is sufficient to use only the selenium client, and
  in its new version (pip install selenium).
